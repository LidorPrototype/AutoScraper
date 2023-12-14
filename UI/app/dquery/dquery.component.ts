import { Component, Inject, Optional } from '@angular/core';
import { UntypedFormBuilder, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ngxCsv } from 'ngx-csv';
import { MatDialog, MAT_DIALOG_DATA } from '@angular/material/dialog'
import { ScheduleDialogComponent } from '../schedule-dialog/schedule-dialog.component';

@Component({
  selector: 'app-dquery',
  templateUrl: './dquery.component.html',
  styleUrls: ['./dquery.component.css']
})
export class DqueryComponent {
 
  loader = false;
  url = "";
  showResult: any = [];
  resultNames: any = [];
  resultValues: any = [];
  showData: any = {};
  linksList:any[] = [];
  link = {
    url:'',
    prefix:''
  }
  queryList:any[] = [];
  query = {
    name:'',
    value:'' 
  }
  metadataList:any[] = [];
  metadata = {
    name:'',
    value:''
  }
  bbody = {};
  bResult:any = [];
  removeHTML = false;
  splitlines = false;
  emptycells = false;
  extentionV = false;
  radioselection = []
  panelOpenState = false;
  arr: string[]= [];
  viewItems: any[] = [];
  state: boolean = false;
  hideSchedule: boolean = false;
  dataToSchedule:any = null;
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

  constructor(private fb: UntypedFormBuilder,private http: HttpClient, public dialog: MatDialog, @Inject(MAT_DIALOG_DATA) @Optional() public data: any) {
    if (data != null && data.Parameters.length > 0) {
      const _data = JSON.parse(data.Parameters[0].parameterValue);
      console.log(`_data: ${_data}`);
      /******************** URL + PREFIX ********************/
      for (let i = 0; i < _data["urls"].length; i++) {
        const url = _data['urls'][i];
        const prefix = _data['prefixes'][i];
        // console.log(`url: ${url}, prefix: ${prefix}`);
        let _link = {
          url: url,
          prefix: prefix
        }
        this.linksList.push(_link);
      }
      /********************** QUERIES ***********************/
      for (const key in _data["queries"]) {
        let _query = {
          name: key,
          value: _data["queries"][key] 
        }
        this.queryList.push(_query);
      }
      /********************* METADATA ***********************/
      for (const key in _data["metadata"]) {
        let _metadata = {
          name: key,
          value: _data["metadata"][key]
        }
        this.metadataList.push(_metadata);
      }
      /********************* PRE DATA ***********************/
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

  showExtention(){
    if(this.splitlines){
      this.extentionV = true;
    }
  }

  updatefield(q:any){
    let tmp = {
      name: this.query.name,
      value: btoa(this.query.value)
    }; 
    console.log("encode tmp: ", tmp)
    this.queryList.push(tmp);
  }

  updateUrlfield(l:any){
    let tmp = {
      url: this.link.url,
      prefix: this.link.prefix
    };
    this.linksList.push(tmp);

  }

  updateMetafield(m:any){
    let tmp = {
      name: this.metadata.name,
      value: this.metadata.value
    };
    this.metadataList.push(tmp);
  }

  removefield(i:number) {
    console.log("decode tmp: ",this.queryList[i].name, atob(this.queryList[i].value))
    console.log(this.queryList[i]);
    this.queryList.splice(i,1);    
  }

  removeUrlfield(i:number) {
    console.log(this.linksList[i]);
    this.linksList.splice(i,1);    
  }

  removeMetafield(i:number) {
    console.log(this.metadataList[i]);
    this.metadataList.splice(i,1);    
  }
  
  showSchedule = true;
  onSubmit(): void {
    this.loader = true;
    this.viewItems = [];
    this.arr= [];
    const qList:any ={};
    this.queryList.forEach(item=>{
      qList[item.name]= item.value;
    })
    console.log(qList)

    const mList:any ={};
    this.metadataList.forEach(item=>{
      mList[item.name]= item.value;
    })
    console.log(mList)
    const urlArr:any =[];
    const prefixArr:any =[];
    this.linksList.forEach(item => {
      urlArr.push(item.url);
      prefixArr.push(item.prefix);
    })
    console.log(urlArr)
    console.log(prefixArr)
    
    const query_model = {
      "queries_model": {
        // "is_xpath": true,
        // "is_bs4": false,
        "urls": urlArr,
        "prefixes": prefixArr,
        "metadata": mList,
        "queries": qList,
        "project": "",
        "out": ""
      }
    };

    try {
      this.loader = true;
      const reqUrl = "https://<INSERT DOMAIN NAME>.azurewebsites.net/post_queries?example=N";
      const headers = { 'content-type': 'application/json'}  
      const body=JSON.stringify(query_model);
      this.bbody = body;
      this.dataToSchedule = body;
      console.log(body)
  
      this.http.post(reqUrl, body,{'headers':headers}).subscribe(data => {
        this.loader = true;
        this.state = true;
        console.log("success: " ,data);
        this.showResult = data;
        this.bResult = this.showResult[0];
        console.log("showResult[0]: ", this.showResult[0])

        this.resultNames = Object.keys(this.showResult[0]);
        console.log("resultNames: ",this.resultNames);
        this.resultValues = Object.values(this.showResult[0]);
        console.log("resultValues: ",this.resultValues);

        const resultObj = this.bResult
        Object.keys(resultObj).forEach(element => {
          this.arr.push(element);
        });
        const firstElement = resultObj[Object.keys(this.bResult)[0]];
        console.log("firstElement:", firstElement);
        if(firstElement !== undefined) {
          Object.keys(firstElement).forEach(key => {
            const temparr: string[] = [];
            temparr.push(key)
            for(let i = 0; i < this.arr.length; i++){
              temparr.push(resultObj[this.arr[i]][key]);
            }
            this.viewItems.push(temparr);
    
          });
        }
        
        console.log("viewItems:", this.viewItems);
        console.log("bResult: ",this.bResult);
        this.showSchedule = false;
        this.loader = false;
      });
      
    } catch (error) {
      this.loader = false;
      this.showSchedule = false;
      console.log("ERROR: ",error);
    }

    this.showData = this.showResult;
  }

  openSchedule(){
    let dialogResult = this.dialog.open(ScheduleDialogComponent,{width:'600px', data:{parameters:this.dataToSchedule,serviceID:4, preData:this.preData}});
    dialogResult.afterClosed().subscribe(result => {
      console.log(`result from dialog:`,result);
    })
  }


  dounloadAsCSV(): void {
    new ngxCsv(this.viewItems, 'query_export',{headers: this.arr});
  }

}