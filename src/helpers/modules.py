import os
import streamlit as st
import github
import logging
import aiofiles
import asyncio

from helpers.base import BaseHelper

logger = logging.getLogger(__name__)


class ModuleHelper(BaseHelper):
    def __init__(self, repo_tags: list[str] | None = ["splash"]):
        super().__init__()
        self.repo_tags = repo_tags
        asyncio.run(self.setup_module_paths())

    async def setup_module_paths(self) -> None:
        repos = await self.get_repos()

        async def process_repo(repo):
            # Get latest commit SHA from main branch
            main_branch = repo.get_branch("main")
            commit_sha = main_branch.commit.sha

            if os.path.exists(
                f"{self.MODULE_DIR}/{repo.full_name.split('/')[-1]}/{commit_sha}"
            ):
                return  # Module already exists for this commit
            file_list = await self.list_repo_files(repo.full_name, path="src")
            if file_list:
                for file in file_list:
                    local_path = f"{self.MODULE_DIR}/{repo.full_name.split('/')[-1]}/{commit_sha}/{file.path.split('/')[-1]}"
                    if not os.path.exists(local_path) and file.path.endswith(".py"):
                        await self.save_file_to_dir(
                            repo_name=repo.full_name,
                            github_path=file.path,
                            local_path=local_path,
                        )

        await asyncio.gather(*(process_repo(repo) for repo in repos))

    async def get_repos(self) -> list[github.Repository.Repository]:
        user = self.git.get_user()
        repos = user.get_repos()
        if self.repo_tags:

            async def filter_repo(repo):
                topics = repo.get_topics()
                return any(tag in topics for tag in self.repo_tags)

            filtered = await asyncio.gather(*(filter_repo(repo) for repo in repos))
            return [repo for repo, keep in zip(repos, filtered) if keep]
        return list(repos)

    async def list_repo_files(
        self, repo_name: str, path: str = ""
    ) -> list[github.ContentFile.ContentFile]:
        repo = self.git.get_repo(repo_name)
        try:
            contents = repo.get_contents(path)
            files = []
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    files.append(file_content)
            return files
        except github.GithubException as e:
            logger.error(f"Error fetching files from {repo_name}/{path}: {e}")
            return []

    async def get_repo_content(self, repo_name: str, path: str) -> str | None:
        repo = self.git.get_repo(repo_name)
        try:
            file_content = repo.get_contents(path)
            return file_content.decoded_content.decode()
        except github.GithubException as e:
            st.error(f"Error fetching content from {repo_name}/{path}: {e}")
            return None

    async def save_file_to_dir(
        self, repo_name: str, github_path: str, local_path: str | None = None
    ) -> None:
        content = await self.get_repo_content(repo_name, github_path)
        if content:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            async with aiofiles.open(local_path, "w") as f:
                await f.write(content)
            logger.info(f"Saved {repo_name}/{github_path} to {local_path}")

    # def _load_module_from_github(
    #     self, repo_name: str, github_path: str, module_path: str
    # ) -> None:
    #     content = self.get_repo_content(repo_name, github_path)
    #     if content:
    #         module_name = module_path.replace("/", ".").rstrip(".py")
    #         spec = importlib.util.spec_from_loader(module_name, loader=None)
    #         module = importlib.util.module_from_spec(spec)
    #         exec(content, module.__dict__)
    #         sys.modules[module_name] = module
    #         logger.info(f"Loaded module {module_name} from {repo_name}/{github_path}")
