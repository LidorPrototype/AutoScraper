import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-testing-ui',
  templateUrl: './testing-ui.component.html',
  styleUrls: ['./testing-ui.component.css']
})
export class TestingUiComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }
  title = "Angular Grid Card View";
  gridColumns = 3;

  toggleGridColumns() {
    this.gridColumns = this.gridColumns === 3 ? 4 : 3;
  }

}
