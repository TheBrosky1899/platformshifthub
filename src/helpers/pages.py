import asyncio
import os
import streamlit as st
from helpers.base import BaseHelper
import random
from streamlit.material_icon_names import ALL_MATERIAL_ICONS


class PageHelper(BaseHelper):
    def __init__(self):
        super().__init__()
        self.page_navigation : st.navigation = {}
        # Automatically initialize navigation asynchronously
        asyncio.run(self._async_init())

    async def _async_init(self):
        """Asynchronous initializer."""
        await self.build_page_navigation()

    async def build_page_navigation(self):
        """Recursively walk module directories to build Streamlit navigation."""
        module_dir = getattr(self, "MODULE_DIR", None) or "src/external_modules"

        nav = {}

        async def process_file(repo_name, commit_sha, file_name, file_path):
            """Process each file found."""
            if file_name.endswith(".py"):
                if repo_name not in nav:
                    nav[repo_name] = []
                nav[repo_name].append(
                    st.Page(
                        page=file_path.replace("src/", ""),
                        url_path=file_path.replace("/", "_").rstrip(".py"),
                    )
                )

        # Walk through repositories and commit directories
        for repo_name in os.listdir(module_dir):
            repo_path = os.path.join(module_dir, repo_name)
            if not os.path.isdir(repo_path):
                continue

            for commit_sha in os.listdir(repo_path):
                sha_path = os.path.join(repo_path, commit_sha)
                if not os.path.isdir(sha_path):
                    continue

                # Only top-level files (no nested folders)
                for file_name in os.listdir(sha_path):
                    file_path = os.path.join(sha_path, file_name)
                    if os.path.isfile(file_path) and file_name.endswith(".py"):
                        await process_file(repo_name, commit_sha, file_name, file_path)

        self.page_navigation = nav

    async def get_page_navigation(self):
        """Return built navigation; build it if needed."""
        if not self.page_navigation:
            await self.build_page_navigation()
        return self.page_navigation
