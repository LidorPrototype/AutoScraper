import { Component, Inject, Optional } from '@angular/core';
import { FormArray, UntypedFormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ngxCsv } from 'ngx-csv/ngx-csv';
import { MatDialog, MAT_DIALOG_DATA } from '@angular/material/dialog'
import { ScheduleDialogComponent } from '../schedule-dialog/schedule-dialog.component';


@Component({
  selector: 'app-draw',
  templateUrl: './draw.component.html',
  styleUrls: ['./draw.component.css']
})

export class DrawComponent {
  name: string = '';
  value: string = '';
  array: any[] = [];
  stopBtn = false;
  loader = false;

  parameters: any = {};
  dataToSchedule: any = null;

  url!: string;
  duplicate!: string;
  responseData: any = [];
  title: any;
  resData: any = {};

  viewItems: any[] = [];
  arr: string[] = [];
  state: boolean = false;
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


  constructor(private fb: UntypedFormBuilder, private http: HttpClient, public dialog: MatDialog, @Inject(MAT_DIALOG_DATA) @Optional() public data: any) {
    if (data != null && data.Parameters.length > 0) {
      const _data = JSON.parse(data.Parameters[0].parameterValue);
      this.url = _data.url;
      this.duplicate = _data.duplications;
      for (const key in _data.parameters) {
        console.log(_data.parameters[key]);
        let tmp = {
          name: key,
          value: _data.parameters[key]
        };
        this.array.push(tmp);
      }
      
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

  updatefield() {
    let tmp = {
      name: this.name,
      value: this.value.split(";")
    };
    this.array.push(tmp);
    this.parameters[tmp.name] = tmp.value;
  }

  removefield(i: number) {
    console.log(this.array[i]);
    this.array.splice(i, 1);
  }

  ynAnsware = [
    { name: 'Yes', value: 'True' },
    { name: 'No', value: 'False' }
  ];

  dounloadAsCSV(): void {
    new ngxCsv(this.viewItems, 'export');
  }

  showSchedule = true;
  onSubmit(): void {
    this.loader = true;
    this.stopBtn = true;

    this.viewItems = [];
    this.arr = [];
    this.state = false;
    console.log("url: ", this.url);
    console.log("duplicate: ", this.duplicate);
    const parm: any = {};
    this.array.forEach(item => {
      parm[item.name] = item.value;
    })
    console.log("parameters:", parm);
    const raw_model = {
      raw_model: {
        url: this.url,
        duplications: this.duplicate,
        parameters: parm
      }

    };

    try {
      this.loader = true;
      const reqUrl = "https://<INSERT DOMAIN NAME>.azurewebsites.net/post_autoscraper";
      const headers = { 'content-type': 'application/json' }
      const body = JSON.stringify(raw_model);
      this.dataToSchedule = body;
      console.log(body)

      this.http.post(reqUrl, body, { 'headers': headers }).subscribe(data => {
        this.state = true;
        const dRes: any = data;
        const b = dRes[1];
        var i = 0
        Object.keys(b).forEach(element => {
          this.arr.push(element);
        });
        const firstElement = b[Object.keys(dRes[1])[0]];

        Object.keys(firstElement).forEach(key => {
          const temparr: string[] = [];
          temparr.push(key)
          for (i = 0; i < this.arr.length; i++) {
            temparr.push(b[this.arr[i]][key]);
          }
          this.viewItems.push(temparr);

        });
        this.showSchedule = false;
        this.stopBtn = false;
        this.loader = false;
      });

    } catch (error) {
      this.loader = false;
    }

  }

  openSchedule() {
    let dialogResult = this.dialog.open(ScheduleDialogComponent, { width: '600px', data: { parameters: this.dataToSchedule, serviceID: 1, preData:this.preData} });
    dialogResult.afterClosed().subscribe(result => {
      console.log(`result from dialog:`, result);
    })
  }

}
