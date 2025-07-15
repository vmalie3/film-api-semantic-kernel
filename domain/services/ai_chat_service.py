import json
import time
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings
from domain.models.requests.film import FilmSummaryRequest
from domain.models.responses import FilmSummaryResponse
from core.config import settings
from fastapi import HTTPException, status
from core.logging import get_logger
from pathlib import Path
import os

logger = get_logger(__name__)

this_dir = Path(__file__).parent
plugins_directory = (this_dir / ".." / ".." / "core" / "prompts").resolve()

class AIService:
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.configuration = settings

    async def ask(self, prompt: str) -> str:
        start_time = time.time()
        logger.debug("Processing AI ask request", prompt_length=len(prompt))
        
        try:
            settings = AzureChatPromptExecutionSettings(
                function_choice_behavior=FunctionChoiceBehavior.Auto(),
            )

            args = KernelArguments(
                settings=settings,
                input=prompt
            )

            chat_plugin = self.kernel.add_plugin(parent_directory=plugins_directory, plugin_name="ChatPlugin")
            chat_function = chat_plugin["Ask"]

            response = await self.kernel.invoke(
                chat_function,
                arguments=args
            )
            
            if response.value is not None and response.value[0] is not None:
                result = response.value[0].content
                duration = time.time() - start_time
                logger.info("AI ask completed", duration_ms=round(duration * 1000, 2), response_length=len(result))
                return result
            else:
                logger.warning("AI ask returned empty response")
                return "No response from AI"
                
        except Exception as e:
            duration = time.time() - start_time
            logger.error("AI ask failed", error=str(e), duration_ms=round(duration * 1000, 2), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process AI request"
            )

    async def film_summary(self, film_summary_request: FilmSummaryRequest) -> FilmSummaryResponse:
        start_time = time.time()
        logger.debug("Processing film summary request", film_id=film_summary_request.film_id)
        
        try:
            settings = AzureChatPromptExecutionSettings(
                function_choice_behavior=FunctionChoiceBehavior.Auto(),
                response_format=FilmSummaryResponse,
            ) 

            args = KernelArguments(
                settings=settings,
                film_id=film_summary_request.film_id
            )

            summarize_plugin = self.kernel.add_plugin(parent_directory=plugins_directory, plugin_name="SummarizePlugin")
            summarize_film_function = summarize_plugin["Film"]

            response = await self.kernel.invoke(
                summarize_film_function,
                arguments=args
            )

            if not response.value or not response.value[0]:
                logger.error("AI film summary returned empty response")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="AI service returned empty response"
                )

            content = response.value[0].content
            
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error("Failed to parse AI response as JSON", error=str(e), content_preview=content[:200])
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="AI response format is invalid"
                )

            try:
                parsed_response = FilmSummaryResponse.model_validate(data)
                duration = time.time() - start_time
                logger.info("Film summary completed", film_id=film_summary_request.film_id, duration_ms=round(duration * 1000, 2))
                return parsed_response
            except Exception as e:
                logger.error("Failed to validate AI response", error=str(e))
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="AI response validation failed"
                )
                
        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            duration = time.time() - start_time
            logger.error("Unexpected error in film summary", film_id=film_summary_request.film_id, error=str(e), duration_ms=round(duration * 1000, 2), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate film summary"
            )
        
        
