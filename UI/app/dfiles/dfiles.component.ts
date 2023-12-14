import { Component, Inject, Optional, OnInit } from '@angular/core';
import { UntypedFormBuilder, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MatDialog, MAT_DIALOG_DATA } from '@angular/material/dialog'
import { ScheduleDialogComponent } from '../schedule-dialog/schedule-dialog.component';


@Component({
  selector: 'app-dfiles',
  templateUrl: './dfiles.component.html',
  styleUrls: ['./dfiles.component.css']
})
export class DfilesComponent implements OnInit {
  downloadUrl = this.fb.group({
    url: [null, Validators.required],
    fileName: [null]
  });
  hideloader = false;;
  responseData = null;
  loader = false;
  tryItLock = false;
  dataToSchedule: any = [];
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
  constructor(private fb: UntypedFormBuilder, private http: HttpClient, public dialog: MatDialog, @Inject(MAT_DIALOG_DATA) @Optional() public data: any, 
  ) {
    if (data != null && data.Parameters.length > 0) {
      this.downloadUrl.controls['url'].setValue(data.Parameters[0].parameterValue.substring(1, data.Parameters[0].parameterValue.length - 1));
      this.downloadUrl.controls['fileName'].setValue(data.Parameters[1].parameterValue.substring(1, data.Parameters[1].parameterValue.length - 1));
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
    this.hideloader = true;
    this.tryItLock = true;
    try {
      var currentUrl = this.downloadUrl.controls['url'].value;
      var currentFileName = this.downloadUrl.controls['fileName'].value;
      console.log("value:", currentUrl);
      var filetype = currentFileName.split(".")[1];
      var splitfilename: String[] = currentUrl.split("/");
      var filename = splitfilename[(splitfilename.length - 1)];
      console.log("filename: ", filename)
      console.log("filetype: ", filetype);
      const requestBody = {
        "api_link": currentUrl,
        "file_name": currentFileName
      }
      console.log(requestBody);
      this.dataToSchedule = requestBody;
      const reqUrl = "https://<INSERT DOMAIN NAME>.azurewebsites.net/post_file?example=N";
      const headers = { 'accept': 'application/json', 'content-type': 'application/json' }
      const body = JSON.stringify(requestBody);
      this.dataToSchedule = body;
      console.log(body)
      
      this.http.post(reqUrl, body, { 'headers': headers, responseType: 'arraybuffer' }).subscribe((response: any) =>
        this.downLoadFile(response, filetype.toString(), currentFileName.toString()
      ))
      
    } catch (error) {
      this.hideloader = false;
    }
  }

  openSchedule() {
    let dialogResult = this.dialog.open(ScheduleDialogComponent, { width: '600px', data: { parameters: this.dataToSchedule, serviceID: 3, preData: this.preData} });
    dialogResult.afterClosed().subscribe((result: any) => {
      console.log(`result from dialog:`, result);
    })
  }

  SendRequest() {
    if (true) {
      console.log(this.downloadUrl.controls['url'].value);
      alert("Request Sent To IT Team");
    }
  }

  downLoadFile(data: any, type: string, name: string) {
    console.log("data:", data);
    this.showSchedule = false;
    this.hideloader = false;
    this.tryItLock = false;
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
    this.hideloader = false;
    console.log("Response",response);
    let header_content = response.headers.get('Content-Disposition');
    let file = header_content.split('=')[1];
    file = file.substring(1, file.length - 1);
    var splitUrl: String[] = file.split(".");
    let extension = splitUrl[splitUrl.length - 1].toLowerCase();
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
    else {
      fileType = 'application/xml';
    }
    return fileType;
  }


}
