import { animate, state, style, transition, trigger } from '@angular/animations';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit, ViewChild, ElementRef, Optional } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSort } from '@angular/material/sort';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { MatDialog } from '@angular/material/dialog';
import { UsersScreen } from '../Models/models';
import { DfilesComponent } from '../dfiles/dfiles.component';
import { DrawComponent } from '../draw/draw.component';
import { lastValueFrom, scheduled } from 'rxjs';
import { DqueryComponent } from '../dquery/dquery.component';
import { MayaComponent } from '../maya/maya.component';
import { OecdComponent } from '../oecd/oecd.component';

@Component({
  selector: 'app-user-requests',
  templateUrl: './user-requests.component.html',
  styleUrls: ['./user-requests.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})

export class UserRequestsComponent implements OnInit {
  displayedColumns: string[] = ['user', 'DAG_Name', 'cron', 'description', 'output_name', 'start_date', 'end_date', 'status', 'actions'];
  actions: string[] = ['Edit', 'Delete Request'];
  viewer: string[] = ['View', 'Email Worker'];
  filters: string[] = ['My Requests', 'All Requests'];
  @ViewChild(MatSort, { static: true }) sort!: MatSort;
  @ViewChild(MatTable, { static: false }) table!: MatTable<any>;
  @ViewChild(MatPaginator, { static: false }) paginator!: MatPaginator;
  @ViewChild('input', { static: true }) input!: ElementRef<HTMLInputElement>;
  preDataSource = new MatTableDataSource<UsersScreen>([]);
  dataSource = new MatTableDataSource<UsersScreen>([]);
  expandedElement!: UsersScreen | null;
  loaded = false;
  touched = false;
  filterValue = "";
  filterInserted = false;
  fullData = {
    "serviceID": "",
    "hideSchedule": false
  };
  authenticated = "<INSERT AUTHENTICATED EMAIL TEST>";

  constructor(private http: HttpClient, public snackBar: MatSnackBar, public dialog: MatDialog) {}

  ngOnInit(): void {
    this.refreshAll();
  }

  refreshAll(): void {
    this.dataSource.data = [];
    this.loaded = false;
    const reqUrl = "https://<INSERT DOMAIN NAME>.azurewebsites.net/azure_datalake_functions?example=N";
    const headers = { 'content-type': 'application/json' }
    const bbody = {
      "functionality": "list_all",
      "table_name": "UserRequests"
    }
    const body = JSON.stringify(bbody);
    console.log(body)

    this.http.post(reqUrl, body, { 'headers': headers }).subscribe(data => {
      this.loaded = true;
      this.touched = false;
      const x = data as object[];
      this.dataSource.data = x[0] as UsersScreen[];
      this.dataSource.data = this.dataSource.data.sort((a, b) => a.status < b.status ? 1 : a.status > b.status ? -1 : 0);
      this.preDataSource.data = this.dataSource.data;
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
      this.input.nativeElement.disabled = false;
    });
  }

  applyFilter(event: Event|string) {
    if (typeof event == 'string') {
      switch (event) {
        case this.filters[0]: // 'My Requests
          this.dataSource.filter = this.authenticated.trim().toLowerCase();
          this.dataSource.data = this.dataSource.filteredData;
          break;
        case this.filters[1]: // All Requests
          this.filterValue = '';
          this.dataSource.data = this.preDataSource.data;
          this.dataSource.filter = this.filterValue.trim().toLowerCase();
          break;
      }
    }else{
      this.filterValue = (event.target as HTMLInputElement).value;
      this.dataSource.filter = this.filterValue.trim().toLowerCase();
    }
    if (this.filterValue.length > 0) {
      this.filterInserted = true;
      this.dataSource.filter = this.filterValue.trim().toLowerCase();
    }else{
      this.filterInserted = false;
    }
    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  async toggleAction(_action: string, element: UsersScreen): Promise<void> {
    if (_action == this.actions[0] || _action == this.viewer[0]) {  /******************************* Edit + View *******************************/
      this.filterInserted = false;
      this.loaded = false;
      this.fullData = await this.retrieveRequestFullData(element);
      let componentService2Edit: Object = Object;
      switch (this.fullData.serviceID) {
        case "1": // Raw
          componentService2Edit = DrawComponent;
          break;
        case "2": // Maya
          componentService2Edit = MayaComponent;
          break;
        case "3": // Api
          componentService2Edit = DfilesComponent;
          break;
        case "4": // Queries
          componentService2Edit = DqueryComponent;
          break;
        case "6": // Oecd
          componentService2Edit = OecdComponent;
          break;
      }
      this.filterInserted = true;
      this.loaded = true;
      this.fullData.hideSchedule = _action == this.viewer[0] ? true: false;
      this.openSchedule(componentService2Edit, this.fullData, !this.fullData.hideSchedule);
    }else if (_action == this.actions[1]) { /************************** Delete *****************************/
      const reqUrl = "https://<INSERT DOMAIN NAME>.azurewebsites.net/azure_datalake_functions?example=N";
      const headers = { 'content-type': 'application/json' }
      const bbody = {
        "functionality": 'delete_request',
        "table_name": "UserRequests",
        "partitionKey": element.PartitionKey,
        "rowKey": element.RowKey
      }
      const body = JSON.stringify(bbody);
      console.log(body)
      console.log('element.status.slice(0, -1): ', element.status.slice(0, -1));
      this.http.get(`https://<INSERT DOMAIN NAME>.azurewebsites.net/manage_dag?partitionKey_=${element.PartitionKey}&rowKey_=${element.RowKey}&action_=delete`).subscribe(req => {
        const req1 = <string[]>req;
        console.log(req1)
        this.http.post(reqUrl, body, { 'headers': headers }).subscribe(data => {
          const data1 = data as string[][];
          console.log(data)
          this.refreshAll();
      });
    });
    }else if (_action == this.viewer[1]){ /************************** Email Worker *****************************/
      let workerEmail = element.user;
      const subject = `שלום רציתי לשאול על הקובץ ${element.output_name}`;
      const body = 'צפיתי בבקשה שלך ונראה שהמידע שאתה מוריד רלוונטי עבורי, הייתי שמח לקבוע פגישה שנדבר על כך.';
      const mailtoLink = `mailto:${workerEmail}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      window.location.href = mailtoLink;
    }
  }

  async retrieveRequestFullData(element: UsersScreen): Promise<any> {
    const reqUrl = "https://<INSERT DOMAIN NAME>.azurewebsites.net/azure_datalake_functions?example=N";
    const headers = { 'content-type': 'application/json' }
    let functionality = 'get_full_request';
    const bbody = {
      "functionality": functionality,
      "table_name": "UserRequests",
      "partitionKey": element.PartitionKey,
      "rowKey": element.RowKey,
      "full": true
    }
    const body = JSON.stringify(bbody);
    let data = await lastValueFrom(this.http.post(reqUrl, body, {'headers': headers}));
    return data;
  }

  async applyAction(element: UsersScreen, actionChosen: boolean): Promise<any> {
    const reqUrl = "https://<INSERT DOMAIN NAME>.azurewebsites.net/azure_datalake_functions?example=N";
    const headers = { 'content-type': 'application/json' }
    let functionality = '';
    if (element.actions == 'Edit') {
      functionality = 'get_full_request'
    } else if (element.status == 'Request Delete') {
      functionality = 'request_delete_request'
    }
    if (element.status == 'Request Delete') {
      return;
    }
    // Edit - get_full_request
    const bbody = {
      "functionality": functionality,
      "table_name": "UserRequests",
      "partitionKey": element.PartitionKey,
      "rowKey": element.RowKey,
      "full": true
    }
    const body = JSON.stringify(bbody);
    console.log(body)
    let data = await lastValueFrom(this.http.post(reqUrl, body, {'headers': headers}));
    return data;
  }

  openSnackBar(message: string, messageType: string): void {
    this.snackBar.open(message, messageType, {
      duration: 5000
    });
  }

  openSchedule(componentToOpen: any, datadata: any, _refresh: boolean = true){
    let dialogResult = this.dialog.open(componentToOpen, {maxHeight: '85vh', data: datadata, panelClass: 'custom-dialog'});
    dialogResult.afterClosed().subscribe(result => {
      console.log(`result from dialog:`,result);
      if(_refresh){
        this.refreshAll();
        this.filterValue = "";
        this.input.nativeElement.value = "";
        this.filterInserted = false;
      }
    })
  }

}
