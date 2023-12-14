import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-summerize',
  templateUrl: './summerize.component.html',
  styleUrls: ['./summerize.component.css']
})
export class SummerizeComponent implements OnInit {

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  textarea = '';
  result: any = null;

  GetSummary() {
    try {
      let headers = new HttpHeaders();
      headers.append('Accept', 'text/html');
      let options = { headers: headers };
      this.http.post('https://<INSERT DOMAIN NAME>.azurewebsites.net/api/summarizeText', { text: this.textarea }, { headers, responseType: 'text'})
        .subscribe(
          data => {
            console.log(data);
            this.result = data;
          }
        )
    } catch (error) {
      console.log(error);
    }
  }
}
