import { Component, Inject, OnInit, Optional } from '@angular/core';
import { UntypedFormBuilder, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MatDialog, MAT_DIALOG_DATA } from '@angular/material/dialog'
import { ScheduleDialogComponent } from '../schedule-dialog/schedule-dialog.component';

@Component({
  selector: 'app-oecd',
  templateUrl: './oecd.component.html',
  styleUrls: ['./oecd.component.css']
})
export class OecdComponent implements OnInit {

  downloadUrl = this.fb.group({
    url: [null, Validators.required],
    SeriesName: [null,Validators.required],
    fileType: [null,Validators.required]
  });

  responseData = null;
  loader = false;
  disableBtn = false;
  dataToSchedule:any = [];
  hideSchedule: boolean = false;
  preData = {
    "DAG_Name": "",
    "DestinationID": "",
    "PartitionKey": "",
    "RowKey": "",
    "cron": "",
    "description": "",
    "start_date": "",
    "end_date": "",
    "output_name": "",
    "serviceID": "",
    "status": "",
    "user": "",
  }

  constructor(private fb: UntypedFormBuilder,  private http: HttpClient, public dialog: MatDialog, @Inject(MAT_DIALOG_DATA) @Optional() public data: any) {
    if (data != null && data.Parameters.length > 0) {
      const _data = JSON.parse(data.Parameters[0].parameterValue);
      this.downloadUrl.controls['url'].setValue(_data["oecd_url"]);
      this.downloadUrl.controls['SeriesName'].setValue(_data["series_type"]);
      
      this.preData["DAG_Name"] = data.DAG_Name;
      this.preData["DestinationID"] = data.DestinationID;
      this.preData["PartitionKey"] = data.PartitionKey;
      this.preData["RowKey"] = data.RowKey;
      this.preData["cron"] = data.cron;
      this.preData["description"] = data.description;
      this.preData["start_date"] = data.start_date;
      this.preData["end_date"] = data.end_date;
      this.preData["output_name"] = data.output_name;
      this.preData["serviceID"] = data.serviceID;
      this.preData["status"] = data.status;
      this.preData["user"] = data.user;
      
      this.hideSchedule = data.hideSchedule;
    }
  }

  ngOnInit(): void {}
    
  showSchedule = true;
  onSubmit() {
    this.disableBtn = true;
    this.loader = true;
    try {

    var currentUrl = this.downloadUrl.controls['url'].value;
    var currentSeriesName = this.downloadUrl.controls['SeriesName'].value;
    var fileType = this.downloadUrl.controls['fileType'].value;
    console.log("value:",currentUrl);

    var splitUrl: String[] = currentUrl.split(".");
    var filetype = currentSeriesName.split(".")[1];

    var splitfilename: String[] = currentUrl.split("/");
    var SeriesName = splitfilename[(splitfilename.length-1)];
    console.log("filename: ",SeriesName)
    console.log("filetype: ",fileType);

    const requestBody = {
      "oecd_model":{
      "oecd_url": currentUrl,
      "series_type": currentSeriesName
      }
    }
    console.log(requestBody);
    this.dataToSchedule = requestBody;    
      const reqUrl = "https://<INSERT DOMAIN NAME>.azurewebsites.net/post_oecd";
      const headers = { 'accept': 'application/json', 'content-type': 'application/json'}  
      const body=JSON.stringify(requestBody);
      this.dataToSchedule = body;
      console.log(body)
  
      this.http.post(reqUrl, body,{'headers':headers,responseType: 'arraybuffer'}).subscribe(response => {
        this.downLoadFile(response, fileType ,SeriesName.toString());
        this.showSchedule = false;
        this.disableBtn = false;
      });
  } catch (error) {
    this.loader = false;
    this.disableBtn = false;
  }   
      
}

  openSchedule(){
    let dialogResult = this.dialog.open(ScheduleDialogComponent,{width:'600px',data:{parameters:this.dataToSchedule,serviceID:6, preData:this.preData}});
    dialogResult.afterClosed().subscribe(result => {
      console.log(`result from dialog:`,result);
    })
  }
 
  SendRequest(){
    if (true) {
      console.log(this.downloadUrl.controls['url'].value);
      alert("Request Sent To IT Team");
    }
  }
  
  downLoadFile(data: any, type: string, name:string) {
    console.log("data:",data);
    let blob = new Blob([data], {
       type: this.createFileType(type),
    });
    const a = document.createElement('a');
    const objectUrl = URL.createObjectURL(blob)
    a.href = objectUrl
    a.download = name;
    a.click();
    URL.revokeObjectURL(objectUrl);
 }

 downloadCFile(response: any) {
  this.loader = false;
  console.log(response);
  let header_content = response.headers.get('Content-Disposition');
  let file = header_content.split('=')[1];
  file = file.substring(1, file.length - 1);
  var splitUrl: String[] = file.split(".");
  let extension = splitUrl[splitUrl.length-1].toLowerCase();
  // It is necessary to create a new blob object with mime-type explicitly set
  // otherwise only Chrome works like it should
  var newBlob = new Blob([response.body], { type: this.createFileType(extension) })
  // For other browsers: 
  // Create a link pointing to the ObjectURL containing the blob.
  const data = window.URL.createObjectURL(newBlob);
  var link = document.createElement('a');
  link.href = data;
  link.download = file;
  link.click();
  setTimeout(() => {
    // For Firefox it is necessary to delay revoking the ObjectURL
    window.URL.revokeObjectURL(data);
  }, 400)
}

createFileType(e: any): string {
  this.loader = false;
  console.log("e:", e);
  let fileType: string = "";
  if (e == 'pdf' || e == 'csv') {
    fileType = `application/${e}`;
  }
  else if (e == 'jpeg' || e == 'jpg' || e == 'png') {
    fileType = `image/${e}`;
  }
  else if (e == 'txt') {
    fileType = 'text/plain';
  }
  else if (e == 'ppt' || e == 'pot' || e == 'pps' || e == 'ppa') {
    fileType = 'application/vnd.ms-powerpoint';
  }
  else if (e == 'pptx') {
    fileType = 'application/vnd.openxmlformats-officedocument.presentationml.presentation';
  }
  else if (e == 'doc' || e == 'dot') {
    fileType = 'application/msword';
  }
  else if (e == 'docx') {
    fileType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
  }
  else if (e == 'xls' || e == 'xlt' || e == 'xla') {
    fileType = 'application/vnd.ms-excel';
  }
  else if (e == 'xlsx') {
    fileType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
  }
  else{
    fileType = 'application/xml';
  }
  return fileType;
}

}
