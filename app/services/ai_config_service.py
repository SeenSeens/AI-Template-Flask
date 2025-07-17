import requests
from langchain_community.chat_models import ChatAnthropic, ChatOpenAI
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from openai import OpenAI

from app import AIConfig
from app.repositories.ai_config_repository import AIConfigRepository


class AIConfigService:
    def __init__(self, repository: AIConfigRepository):
        self.repository = repository

    # langchain_loader.py
    def _get_openai_models(self, api_key):

        client = OpenAI(api_key=api_key)
        try:
            response = client.models.list()
            return [model.id for model in response.data]
        except Exception:
            raise ValueError("API Key không hợp lệ hoặc không phải của OpenAI")

    def _get_google_models(self, api_key):
        try:
            model = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-1.5-flash")
            model.invoke("ping")
            return [
                "gemini-pro",
                "gemini-pro-vision",  # hỗ trợ hình ảnh (nếu có)
                "gemini-1.5-pro-preview",  # nếu bạn đã có quyền
                "gemini-1.5-flash-preview",
                "gemini-1.5-flash"
            ]
        except Exception as e:
            print("Google Gemini error:", e)
            raise ValueError("API Key không hợp lệ hoặc không phải của Google")

    def _get_anthropic_models(self, api_key):
        try:
            model = ChatAnthropic(api_key=api_key, model="claude-3-opus-20240229")
            model.invoke("Hi")
            return ["claude-3-opus-20240229", "claude-3-sonnet", "claude-3-haiku"]
        except Exception:
            raise ValueError("API Key không hợp lệ hoặc không phải của Anthropic")



    def _get_huggingface_models(self, api_key, task: str = "text-generation", limit: int = 50):
        """
        Fetch real-time Hugging Face models via API key and task (e.g., text-generation).
        """
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        params = {
            "limit": limit,
            "pipeline_tag": task,  # task = "text-generation", "summarization", etc.
            "sort": "downloads"
        }

        try:
            response = requests.get("https://huggingface.co/api/models", headers=headers, params=params)
            if response.status_code != 200:
                raise ValueError("API Key không hợp lệ hoặc không có quyền truy cập Hugging Face API.")

            models = response.json()

            # Chỉ lấy các model công khai hỗ trợ tác vụ mong muốn
            model_list = []
            for model in models:
                model_list.append({
                    "id": model.get("modelId"),
                    "likes": model.get("likes", 0),
                    "downloads": model.get("downloads", 0),
                    "tags": model.get("tags", []),
                    "pipeline_tag": model.get("pipeline_tag"),
                    "private": model.get("private", False),
                    "author": model.get("author", "unknown"),
                    "cardData": model.get("cardData", {})
                })

            return model_list

        except Exception as e:
            print("Error fetching Hugging Face models:", e)
            raise ValueError("Không thể lấy danh sách mô hình từ Hugging Face.")

    def fetch_models(self, api_key: str, provider: str):
        if provider.lower() == 'openai':
            return self._get_openai_models(api_key)
        elif provider.lower() == 'gemini':
            return self._get_google_models(api_key)
        elif provider.lower() == 'anthropic':
            return self._get_anthropic_models(api_key)
        elif provider.lower() == 'huggingface':
            return self._get_huggingface_models(api_key, task="text-generation")
        else:
            raise ValueError("Provider không hợp lệ")


    # Lưu cấu hình AI vào DB
    # def validate_and_save_config(self, data: dict, user_id: int):
    #     required_fields = ['provider', 'api_key', 'model_name']
    #     for field in required_fields:
    #         if not data.get(field):
    #             return False, f"Trường {field} là bắt buộc."
    #
    #     if not self._test_api_key(data['provider'], data['api_key'], data['model_name']):
    #         return False, "API key hoặc model không hợp lệ."
    #
    #     try:
    #         self.repository.save_or_update_config(user_id, data)
    #         return True, "Cấu hình đã được lưu thành công."
    #     except Exception as e:
    #         return False, f"Lỗi khi lưu: {str(e)}"

    def _test_api_key(self, provider, api_key, model_name):
        try:
            if provider.lower() == 'openai':
                llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name)
                llm.invoke("ping")
            elif provider.lower() == 'gemini':
                llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name)
                llm.invoke("ping")
            elif provider.lower() == 'anthropic':
                llm = ChatAnthropic(api_key=api_key, model=model_name)
                llm.invoke("ping")
            elif provider.lower() == 'huggingface':
                try:
                    llm = HuggingFaceHub(
                        huggingfacehub_api_token=api_key,
                        repo_id=model_name
                    )
                    llm.invoke("ping")
                except Exception:
                    return False

            return True
        except Exception:
            return False

    def get_ai_config_id(self, id_ai_config):
        return self.repository.get_ai_config_id(id_ai_config)

    def get_user_config(self, user_id):
        return self.repository.get_config_by_user(user_id)

    def create_ai_config(self, **kwargs):
        return self.repository.create_ai_config(**kwargs)

    def update_ai_config(self, id_ai_config, **kwargs):
        return self.repository.update_ai_config(id_ai_config, **kwargs)

    def delete_ai_config(self, id_ai_config):
        return self.repository.delete_ai_config(id_ai_config)

    def get_all_configs(self):
        return self.repository.get_all_configs()

    def generate_content_with_gemini(self, prompt: str, user_id: int) -> str:
        config = self.repository.get_config_by_user_and_provider(user_id, 'gemini')

        if not config:
            raise Exception("Bạn chưa cấu hình Gemini hoặc cấu hình không hợp lệ")

        try:
            llm = ChatGoogleGenerativeAI(
                model=config.model_name,
                google_api_key=config.api_key,
                temperature=config.temperature,
                top_p=config.top_p,
                max_output_tokens=int(config.max_tokens),
            )

            # Tạo Prompt Template chuyên cho blog
            templates = {
                "title": PromptTemplate.from_template(
                    'Viết lại tiêu đề hấp dẫn, ngắn gọn từ: "{title}"'),
                "summary": PromptTemplate.from_template(
                    'Tóm tắt ngắn gọn nội dung của một bài viết với tiêu đề: "{title}"'),
                "content": PromptTemplate.from_template("""
                    Bạn là một blogger chuyên nghiệp. Viết một bài blog chi tiết, hấp dẫn với tiêu đề:
                    "{title}"

                    Nội dung cần có mở bài, thân bài, kết bài, ngôn ngữ thân thiện, thu hút người đọc.
                """)
            }
            result = {}
            for key, template in templates.items():
                chain = template | llm | StrOutputParser()
                response = chain.invoke({"title": prompt})
                result[key] = response.content if hasattr(response, 'content') else str(response)

            return result

        except Exception as e:
            print("Gemini invoke error:", e)
            raise Exception("Không thể tạo nội dung với Gemini. Vui lòng kiểm tra lại API key hoặc model.")