import { animate, state, style, transition, trigger } from '@angular/animations';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit, ViewChild, TemplateRef } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSort } from '@angular/material/sort';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { LogsRequest, ScrapeRequest } from '../Models/models';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-logs-screen',
  templateUrl: './logs-screen.component.html',
  styleUrls: ['./logs-screen.component.css'],
  animations: [],
})

export class LogsScreenComponent implements OnInit {
  displayedColumns: string[] = ['RequestIP', 'ServiceName', 'RequestParameters', 'Date', 'Source', 'Error'];
  @ViewChild(MatSort, { static: true }) sort!: MatSort;
  @ViewChild(MatTable, { static: false }) table!: MatTable<any>;
  @ViewChild(MatPaginator, { static: false }) paginator!: MatPaginator;
  dataSource = new MatTableDataSource<LogsRequest>([]);
  expandedElement!: ScrapeRequest | null;
  loaded = false;
  touched = false;
  filterInserted = false;

  constructor(private http: HttpClient, public snackBar: MatSnackBar, private dialog: MatDialog) {}

  openDialogWithTemplateRef(templateRef: TemplateRef<any>) {
    this.dialog.open(templateRef, {
      maxWidth: '50%'
  });
  }

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
      "table_name": "LogsTable"
    }
    const body = JSON.stringify(bbody);
    console.log(body)
    this.http.post(reqUrl, body, { 'headers': headers }).subscribe(data => {
      this.loaded = true;
      this.touched = false;
      const x = data as object[];
      this.dataSource.data = x[0] as LogsRequest[];
      this.dataSource.data = this.dataSource.data.sort((a, b) => a.Date < b.Date ? 1 : a.Date > b.Date ? -1 : 0)
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    if (filterValue.length > 0) {
      this.filterInserted = true;
    }else{
      this.filterInserted = false;
    }
    this.dataSource.filter = filterValue.trim().toLowerCase();
    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  openSnackBar(message: string, messageType: string): void {
    this.snackBar.open(message, messageType, {
      duration: 5000
    });
  }

}
