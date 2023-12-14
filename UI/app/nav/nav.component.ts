import { Component, ViewChild } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css']
})
export class NavComponent {

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  constructor(private breakpointObserver: BreakpointObserver) {}

  showDesc = false;
  showDropdown = false;
  toggleDropdown() {
    this.showDropdown = !this.showDropdown;
  }
  optionSelected(option: string) {
    // Implement what should happen when an option is selected
    console.log('Selected Option:', option);
    // You can add more logic here as needed.
  }

  hoveredRoute: any | null = null;

  isHovered(route: string): boolean {
    return this.hoveredRoute === route;
  }

  setHoveredRoute(route: string | null): void {
    this.hoveredRoute = route || null;
  }

  ngOnInit() {
    //this.breakpoint = (window.innerWidth <= 800) ? 1 : 4;
    if(window.innerWidth <= 800){
      this.showDesc = false
    }
    else{
      this.showDesc = true;
    }
  }
  
  onResize(event:any) {
    if(event.target.innerWidth <= 800){
      this.showDesc = false
    }
    else{
      this.showDesc = true;
    }
  }

}
