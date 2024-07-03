from src.api.external_integration.zapcap_client import ZapCapClient
from src.model.render_options import RenderOptions

class ZapCapService:

    def __init__(self):
        self.zap_cap_client = ZapCapClient()

    def create_video_task(self, video_id: str, 
                          template_id: str, 
                          auto_approve: bool, 
                          language: str, 
                          render_options: RenderOptions):
        return self.zap_cap_client.create_video_task(video_id, 
                                                     template_id, 
                                                     auto_approve,  
                                                     language, 
                                                     render_options)

     
    def get_templates(self):
        return self.zap_cap_client.get_templates()
    
    def upload_video(self, file):
        return self.zap_cap_client.upload_video(file)
    
    def get_video_task(self, video_id, task_id):
        return self.zap_cap_client.get_video_task(video_id, task_id) 