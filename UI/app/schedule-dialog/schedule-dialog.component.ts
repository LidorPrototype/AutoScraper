import { Component, OnInit, inject, Inject } from '@angular/core';
import { UntypedFormBuilder, UntypedFormControl, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MatDialogClose, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog'

@Component({
  selector: 'app-schedule-dialog',
  templateUrl: './schedule-dialog.component.html',
  styleUrls: ['./schedule-dialog.component.css']
})
export class ScheduleDialogComponent implements OnInit {

  responseMessage: any = null;
  responsebool = true;
  scheduleModel = this.fb.group({
    cron: [null, Validators.required],
    start_date: [null, Validators.required],
    end_date: [null, Validators.required],
    DestinationID: [null, Validators.required],
    serviceID: [null],
    output_name: [null, Validators.required],
    description: [null, [Validators.required, Validators.pattern('^[ A-Za-z0-9א-ת!_%,.]+')]],
    user: new UntypedFormControl('', [Validators.required, Validators.pattern("^[A-Za-z0-9._%+-]+@boi+\\.+org+\\.+il$")]),
    parameters: [null]//,
    //Base64: [null]
  })
  toCreate: boolean = true;
  partitionKey: number | null = null;
  rowKey: number | null = null;

  constructor(private fb: UntypedFormBuilder, private http: HttpClient, @Inject(MAT_DIALOG_DATA) public data: any) {
    if (data.preData != null && data.preData["DAG_Name"].length > 1) {
      this.scheduleModel.controls["cron"].setValue(data.preData["cron"]);
      this.scheduleModel.controls["start_date"].setValue(data.preData["start_date"]);
      this.scheduleModel.controls["end_date"].setValue(data.preData["end_date"]);
      let tmpName = this.Destination.find(item => item.value === parseInt(data.preData["DestinationID"], 10))?.name;
      this.scheduleModel.controls["DestinationID"].setValue(tmpName);
      this.scheduleModel.controls["serviceID"].setValue(data.preData["serviceID"]);
      this.scheduleModel.controls["output_name"].setValue(data.preData["output_name"]);
      this.scheduleModel.controls["description"].setValue(data.preData["description"]);
      this.scheduleModel.controls["user"].setValue(data.preData["user"]);
      this.toCreate = false;
      this.partitionKey = data.preData["PartitionKey"];
      this.rowKey = data.preData["RowKey"];
    }
  }

  ngOnInit(): void {
    console.log(this.data);
  }

  Destination = [
    // {name:"Cloud",value:1},
    { name: "<INSERT NAME>", value: 2 }
  ]

  hasFourSpaces(str: string): boolean {
    if (str === "@yearly" || str === "@monthly" || str === "@weekly" || str === "@daily" || str === "@hourly") return true;
    else {
      const spaceCount = (str.match(/ /g) || []).length;
      return spaceCount === 4;
    }
  }

  checkOutputName(str: string): boolean {
    const regex = /^[a-zA-Z0-9_]+_autoPrivate\.[a-zA-Z0-9_]+$/;
    return regex.test(str);
  }

  ScheduleRequest(): any {
    if (!this.hasFourSpaces(this.scheduleModel.value["cron"])) {
      alert("Please check cron value");
      return;
    }

    if (!this.checkOutputName(this.scheduleModel.value["output_name"])) {
      alert("Output FileName must be in *_autoPrivate.* format");
      return;
    }

    if (this.scheduleModel.value["start_date"] > this.scheduleModel.value["end_date"]){
      alert("Start date must be before end date");
      return;
    }

    const RequestData = {
      "functionality": this.toCreate ? "create_request" : "update_request",
      "special_access": "",
      "table_name": this.toCreate ? "" : "UserRequests",
      "entity": this.scheduleModel.value,
      "partitionKey": this.partitionKey,
      "rowKey": this.rowKey,
      "src": true
    };
    //debugger;
    console.log("before - RequestData:", RequestData);
    // Create Base64 Object
    var Base64 = {
      _keyStr: "<INSERT KEY ENCODED>",
      encode: function (e: any) { var t = ""; var n, r, i, s, o, u, a; var f = 0; e = Base64._utf8_encode(e); while (f < e.length) { n = e.charCodeAt(f++); r = e.charCodeAt(f++); i = e.charCodeAt(f++); s = n >> 2; o = (n & 3) << 4 | r >> 4; u = (r & 15) << 2 | i >> 6; a = i & 63; if (isNaN(r)) { u = a = 64 } else if (isNaN(i)) { a = 64 } t = t + this._keyStr.charAt(s) + this._keyStr.charAt(o) + this._keyStr.charAt(u) + this._keyStr.charAt(a) } return t }, decode: function (e: string) { var t = ""; var n, r, i; var s, o, u, a; var f = 0; e = e.replace(/[^A-Za-z0-9\+\/\=]/g, ""); while (f < e.length) { s = this._keyStr.indexOf(e.charAt(f++)); o = this._keyStr.indexOf(e.charAt(f++)); u = this._keyStr.indexOf(e.charAt(f++)); a = this._keyStr.indexOf(e.charAt(f++)); n = s << 2 | o >> 4; r = (o & 15) << 4 | u >> 2; i = (u & 3) << 6 | a; t = t + String.fromCharCode(n); if (u != 64) { t = t + String.fromCharCode(r) } if (a != 64) { t = t + String.fromCharCode(i) } } t = Base64._utf8_decode(t); return t }, _utf8_encode: function (e: string) { e = e.replace(/\r\n/g, "\n"); var t = ""; for (var n = 0; n < e.length; n++) { var r = e.charCodeAt(n); if (r < 128) { t += String.fromCharCode(r) } else if (r > 127 && r < 2048) { t += String.fromCharCode(r >> 6 | 192); t += String.fromCharCode(r & 63 | 128) } else { t += String.fromCharCode(r >> 12 | 224); t += String.fromCharCode(r >> 6 & 63 | 128); t += String.fromCharCode(r & 63 | 128) } } return t }, _utf8_decode: function (e: string) { var t = ""; var n = 0; var r = 0; var c1 = 0; var c2 = 0; while (n < e.length) { r = e.charCodeAt(n); if (r < 128) { t += String.fromCharCode(r); n++ } else if (r > 191 && r < 224) { c2 = e.charCodeAt(n + 1); t += String.fromCharCode((r & 31) << 6 | c2 & 63); n += 2 } else { c2 = e.charCodeAt(n + 1); const c3 = e.charCodeAt(n + 2); t += String.fromCharCode((r & 15) << 12 | (c2 & 63) << 6 | c3 & 63); n += 3 } } return t }
    }
    this.scheduleModel.value.parameters = Base64.encode(this.data.parameters);
    this.scheduleModel.value.serviceID = this.data.serviceID
    console.log("after - RequestData:", RequestData);
    if (this.scheduleModel.valid) {
      console.log('scheduleModel valid')
    }
    else {
      console.log('scheduleModel invalid!!!!')
    }

    try {
      const reqUrl = "https://<INSERT DOMAIN NAME>.azurewebsites.net/azure_datalake_functions?example=N";
      const headers = { 'content-type': 'application/json' }
      const body = JSON.stringify(RequestData);
      console.log(body)
      this.responseMessage = "Sending Request For Schedule...";
      console.log("success: ", this.responseMessage);
      this.responsebool = false;
      this.http.post(reqUrl, body, { 'headers': headers }).subscribe(data => {
        console.log("success: ", data);
        const resData: any = data;
        // debugger
        this.responseMessage = resData[0][0].split(':')[0].trim();
      });

    } catch (error) {
      console.log("ERROR: ", error);
      this.responsebool = false;
      this.responseMessage = error;
    }
    finally {
      this.responsebool = false;
    }
  }
}
