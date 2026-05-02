"""Workflow ingestion and normalization"""

import logging
import re
from typing import Any, Dict, List
import httpx

logger = logging.getLogger(__name__)


class WorkflowIngestion:
    """Handles workflow input ingestion from various sources"""
    
    async def ingest(self, workflow_input: str, source_type: str) -> Dict[str, Any]:
        """
        Ingest workflow from various sources and normalize.
        
        Args:
            workflow_input: Workflow content or URL
            source_type: Type of input (text, github, file)
        
        Returns:
            Normalized workflow data
        """
        logger.info(f"Ingesting workflow from {source_type}")
        logger.info(f"Workflow input: {workflow_input[:100]}..." if len(workflow_input) > 100 else f"Workflow input: {workflow_input}")
        
        if source_type == "text":
            result = await self._ingest_text(workflow_input)
        elif source_type == "github":
            result = await self._ingest_github(workflow_input)
        elif source_type == "file":
            result = await self._ingest_file(workflow_input)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
        
        logger.info(f"Ingestion complete. Result keys: {list(result.keys())}")
        return result
    
    async def _ingest_text(self, text: str) -> Dict[str, Any]:
        """Ingest from text description"""
        logger.info(f"Processing text input ({len(text)} characters)")
        return {
            "source": "text",
            "content": text,
            "structure": {},
            "description": text
        }
    
    async def _ingest_github(self, repo_url: str) -> Dict[str, Any]:
        """Ingest from GitHub repository"""
        logger.info(f"Fetching workflows from GitHub: {repo_url}")
        
        # Extract owner and repo from URL
        match = re.match(r'https?://github\.com/([^/]+)/([^/]+)', repo_url)
        if not match:
            raise ValueError(f"Invalid GitHub URL format: {repo_url}")
        
        owner, repo = match.groups()
        repo = repo.rstrip('/')  # Remove trailing slash if present
        
        logger.info(f"Repository: {owner}/{repo}")
        
        # Fetch workflow files from GitHub
        workflows = await self._fetch_github_workflows(owner, repo)
        
        if not workflows:
            logger.warning(f"No workflows found in {owner}/{repo}")
            return {
                "source": "github",
                "repo_url": repo_url,
                "owner": owner,
                "repo": repo,
                "workflows": [],
                "structure": {},
                "description": f"GitHub repository {owner}/{repo} - No GitHub Actions workflows found in .github/workflows/"
            }
        
        # Build description from workflows
        workflow_descriptions = []
        for wf in workflows:
            workflow_descriptions.append(f"- {wf['name']}: {wf['path']}")
        
        description = f"""GitHub Repository: {owner}/{repo}
Found {len(workflows)} workflow(s):
{chr(10).join(workflow_descriptions)}

Workflow Contents:
{chr(10).join([f"=== {wf['name']} ==={chr(10)}{wf['content']}{chr(10)}" for wf in workflows])}
"""
        
        logger.info(f"Successfully fetched {len(workflows)} workflows")
        
        return {
            "source": "github",
            "repo_url": repo_url,
            "owner": owner,
            "repo": repo,
            "workflows": workflows,
            "structure": {"workflow_count": len(workflows)},
            "description": description
        }
    
    async def _fetch_github_workflows(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """Fetch workflow files from GitHub repository"""
        from app.config import settings
        
        workflows = []
        
        # GitHub API endpoint for repository contents
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/.github/workflows"
        
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ProcessDoctor"
        }
        
        # Add GitHub token if available
        if settings.github_token:
            headers["Authorization"] = f"token {settings.github_token}"
            logger.info("Using GitHub token for authentication")
        else:
            logger.warning("No GitHub token - API rate limits will be restrictive")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Get list of workflow files
                logger.info(f"Fetching workflow list from: {api_url}")
                response = await client.get(api_url, headers=headers)
                response.raise_for_status()
                files = response.json()
                
                logger.info(f"Found {len(files)} files in .github/workflows/")
                
                # Fetch content of each YAML workflow file
                for file_info in files:
                    if file_info['name'].endswith(('.yml', '.yaml')):
                        logger.info(f"Fetching workflow: {file_info['name']}")
                        
                        # Get file content
                        content_response = await client.get(file_info['download_url'], headers=headers)
                        content_response.raise_for_status()
                        content = content_response.text
                        
                        workflows.append({
                            "name": file_info['name'],
                            "path": file_info['path'],
                            "content": content,
                            "size": file_info['size']
                        })
                        
                        logger.info(f"  ✓ Fetched {file_info['name']} ({file_info['size']} bytes)")
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning(f"Repository or workflows directory not found: {owner}/{repo}")
            elif e.response.status_code == 403:
                logger.error("GitHub API rate limit exceeded or access denied")
            else:
                logger.error(f"GitHub API error: {e.response.status_code} - {e.response.text}")
            raise ValueError(f"Failed to fetch workflows from GitHub: {str(e)}")
        except Exception as e:
            logger.error(f"Error fetching GitHub workflows: {str(e)}")
            raise ValueError(f"Failed to fetch workflows: {str(e)}")
        
        return workflows
    
    async def _ingest_file(self, file_path: str) -> Dict[str, Any]:
        """Ingest from file"""
        # TODO: Implement file reading
        return {
            "source": "file",
            "file_path": file_path,
            "structure": {}
        }

# Made with Bob
