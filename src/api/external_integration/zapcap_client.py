from settings import ZAP_CAP_API_KEY, ZAP_CAP_URI
from src.model.render_options import RenderOptions
import http.client
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

class ZapCapClient:
    def __init__(self):
        self.conn = http.client.HTTPSConnection(ZAP_CAP_URI)
        self.api_key = ZAP_CAP_API_KEY

    def upload_video(self, file):

        encoder = MultipartEncoder(
            fields={"video": ("video.mp4", file.read(), "video/mp4")}
        )

        headers = {
            'Content-Type': encoder.content_type,
            'X-Api-Key': self.api_key
        }

        self.conn.request("POST", "/videos", headers=headers, body=encoder)

        res = self.conn.getresponse()
        return res.read()

    def get_templates(self):
        headers = {
            'Content-Type': "application/json",
            'X-Api-Key': f"{self.api_key}"
        }

        self.conn.request("GET", "/templates", headers=headers)

        res = self.conn.getresponse()
        return res.read()

    def create_video_task(self, video_id: str, 
                          template_id: str, 
                          auto_approve: bool, 
                          language: str, 
                          render_options: RenderOptions):
        payload = {
            "templateId": template_id,
            "autoApprove": auto_approve,
            #TODO add transcript_task_id
            "language": language,
            "renderOptions": render_options.to_json()
        }

        headers = {
            'Content-Type': "application/json",
            'X-Api-Key': f"{self.api_key}"
        }

        self.conn.request("POST", f"/videos/{video_id}/task", body=json.dumps(payload), headers=headers)

        res = self.conn.getresponse()
        return res.read()

    def get_video_task(self, video_id, task_id):
        headers = {
            'X-Api-Key': self.api_key
        }

        self.conn.request("GET", f"/videos/{video_id}/task/{task_id}", headers=headers)

        res = self.conn.getresponse()
        return res.read()

    #with open("src/video.mp4", 'rb') as finput:
    #    response = requests.put("https://" + ZAP_CAP_URI + "/videos", data=finput)
    #    print(response.json())
    #import ssl
    #from urllib.request import urlopen
    #data = urlopen('https://www.howsmyssl.com/a/check', context=ssl._create_unverified_context()).read()
    #print(data.decode("utf-8"))
    #video_path = "src/video.mp4"
    #res = upload_video(video_path)
    #print(res)
    #templates_res = get_templates()
    #print(templates_res)
    #video_id = json.loads(res)["id"]
    #print(video_id)
    #video_id = "674bb024-21bc-4458-85e2-22983855eb7b"
    #template_id = "cfa6a20f-cacc-4fb6-b1d0-464a81fed6cf"
    #res = create_video_task(video_id, template_id, True, True, "en", RenderOptions())
    #print(res)
    #task_id = "593e9de0-d2d0-4efd-afcb-5ba8ac7dc046"
    #res = get_task(video_id, task_id)
    #print(res)

