import { animate, state, style, transition, trigger } from '@angular/animations';
import { HttpClient } from '@angular/common/http';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatPaginator } from '@angular/material/paginator';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSort } from '@angular/material/sort';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { lastValueFrom } from 'rxjs';
import { DfilesComponent } from '../dfiles/dfiles.component';
import { DqueryComponent } from '../dquery/dquery.component';
import { DrawComponent } from '../draw/draw.component';
import { MayaComponent } from '../maya/maya.component';
import { ScrapeRequest, UsersScreen } from '../Models/models';
import { OecdComponent } from '../oecd/oecd.component';

@Component({
  selector: 'app-manage-control',
  templateUrl: './manage-control.component.html',
  styleUrls: ['./manage-control.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})

export class ManageControlComponent implements OnInit {

  displayedColumns: string[] = ['DAG_Name', 'cron', 'description', 'output_name', 'start_date', 'end_date', 'user', 'status', 'changeStatus', 'Action'];
  statuses: string[] = ['created', 'disabled', 'deleted']; //pending
  @ViewChild(MatSort, { static: true }) sort!: MatSort;
  @ViewChild(MatTable, { static: false }) table!: MatTable<any>;
  @ViewChild(MatPaginator, { static: false }) paginator!: MatPaginator;
  @ViewChild('input', { static: true }) input!: ElementRef<HTMLInputElement>;
  dataSource = new MatTableDataSource<ScrapeRequest>([]);
  expandedElement!: ScrapeRequest | null;
  loaded = false;
  touched = false;
  filterInserted = false;
  filterValue = "";
  fullData = {
    "serviceID": "",
    "hideSchedule": false
  };

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
      this.dataSource.data = x[0] as ScrapeRequest[];

      this.dataSource.data = this.dataSource.data.sort((a, b) => a.status < b.status ? 1 : a.status > b.status ? -1 : 0)
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    });
  }

  async toggleAction(_action: 'View', element: UsersScreen): Promise<void> {
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
    this.fullData.hideSchedule = true;
    this.openSchedule(componentService2Edit, this.fullData, !this.fullData.hideSchedule);
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

  toggleStatus(element: ScrapeRequest, newValue: string): void {
    this.changeStatus(element);
  }

  applyFilter(event: Event) {
    this.filterValue = (event.target as HTMLInputElement).value;

    if (this.filterValue.length > 0) {
      this.filterInserted = true;
    }else{
      this.filterInserted = false;
    }

    this.dataSource.filter = this.filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  changeStatus(element: ScrapeRequest): void {
    const reqUrl = "https://<INSERT DOMAIN NAME>.azurewebsites.net/azure_datalake_functions?example=N";
    const headers = { 'content-type': 'application/json' }
    let functionality = '';
    if (element.status == 'created') {
      functionality = 'approve_request'
    } else if (element.status == 'disabled') {
      functionality = 'disable_request'
    } else if (element.status == 'deleted') {
      functionality = 'delete_request'
    }
    const bbody = {
      "functionality": functionality,
      "table_name": "UserRequests",
      "partitionKey": element.PartitionKey,
      "rowKey": element.RowKey
    }
    const body = JSON.stringify(bbody);
    console.log(body)

    this.http.get(`https://<INSERT DOMAIN NAME>.azurewebsites.net/manage_dag?partitionKey_=${element.PartitionKey}&rowKey_=${element.RowKey}&action_=${element.status.slice(0, -1)}`).subscribe(req => {
        const req1 = <string[]>req;
        console.log(req1)
        this.http.post(reqUrl, body, { 'headers': headers }).subscribe(data => {
          const data1 = data as string[][];
          console.log(data)
          this.refreshAll();
      });
    });
  }

  saveChanges(element: ScrapeRequest): void {
    this.changeStatus(element);
  }

  saveAllChanges(): void {
    this.dataSource.data.forEach((element: ScrapeRequest) => {
      if (element.changed)
        this.changeStatus(element);
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

  openSnackBar(message: string, messageType: string): void {
    this.snackBar.open(message, messageType, {
      duration: 5000
    });
  }

}
