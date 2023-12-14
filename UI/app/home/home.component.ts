import { Component } from '@angular/core';
import { map } from 'rxjs/operators';
import { Breakpoints, BreakpointObserver } from '@angular/cdk/layout';

export interface PeriodicElement {
  scrapperType: string;
  position: number;
  count: number;
  symbol: string;
  success: number;
  failed: number;
}

const ELEMENT_DATA: PeriodicElement[] = [
  {position: 1, scrapperType: 'raw', count: 10, symbol: 'H', success: 5,failed: 5},
  {position: 2, scrapperType: 'raw', count: 40, symbol: 'He', success: 25,failed: 15},
  {position: 3, scrapperType: 'raw', count: 60, symbol: 'Li', success: 58,failed: 2},
  {position: 4, scrapperType: 'api', count: 90, symbol: 'Be', success: 90,failed: 0},
  {position: 5, scrapperType: 'api', count: 20, symbol: 'B', success: 0,failed: 20},
  {position: 6, scrapperType: 'api', count: 12, symbol: 'C', success: 10,failed: 2},
  {position: 7, scrapperType: 'query', count: 14, symbol: 'N', success: 14,failed: 0},
  {position: 8, scrapperType: 'query', count: 15, symbol: 'O', success: 3,failed: 12},
  {position: 9, scrapperType: 'Maya', count: 18, symbol: 'F', success: 10,failed: 8},
  {position: 10, scrapperType: 'Maya', count: 20, symbol: 'Ne', success: 20,failed: 0}
];

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  /** Based on the screen size, switch from standard to one column per row */
  displayedColumns: string[] = ['position', 'scrapperType', 'count', 'symbol','success','failed'];
  dataSource = ELEMENT_DATA;

  constructor(private breakpointObserver: BreakpointObserver) {}
  breakpoint: number | undefined;
  
  ngOnInit() {
    if(window.innerWidth <= 1200 && window.innerWidth > 800){
      this.breakpoint = 2
    }
    else if(window.innerWidth <= 800){
      this.breakpoint = 1
    }
    else{
      this.breakpoint = 4;
    }
  }
  
  onResize(event:any) {
    if(event.target.innerWidth <= 1200 && event.target.innerWidth > 800){
      this.breakpoint = 2
    }
    else if(event.target.innerWidth <= 800){
      this.breakpoint = 1
    }
    else{
      this.breakpoint = 4;
    }
  }

}
