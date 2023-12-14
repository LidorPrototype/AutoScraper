import { Component } from '@angular/core';
import { UntypedFormBuilder, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-dapi',
  templateUrl: './dapi.component.html',
  styleUrls: ['./dapi.component.css']
})
export class DapiComponent {
  dapiForm = this.fb.group({
    api: [null, Validators.required],
    filename: [null, Validators.required],
    format: [null, Validators.required],
  });
  url = null;
  filename = null;
  format = null;
  loader = false;

  formats = [
    {name: 'Default', value: 'DEF'},
    {name: 'Json', value: 'JSON'},
    {name: 'Csv', value: 'CSV'},
    {name: 'Txt', value: 'TXT'},
    {name: 'Html', value: 'HTML'},
    {name: 'Doc', value: 'DOC'},
    {name: 'Docx', value: 'DOCX'},
    {name: 'Pdf', value: 'PDF'}
  ];

  constructor(private fb: UntypedFormBuilder,private http: HttpClient) {}

  onSubmit(): void {
    this.url = this.dapiForm.controls['api'].value;
    this.filename = this.dapiForm.controls['filename'].value;
    this.format = this.dapiForm.controls['format'].value;
    this.http.post<any>("https://<INSERT DOMAIN NAME>.azurewebsites.net/post_file", { api_link: this.dapiForm.controls['api'].value }).subscribe(data => {
        console.log(data);
    })
  }

  SendRequest(){
    if (true) {
      console.log(this.dapiForm.value);
      alert("Request Sent To IT Team");
    }
  }
}
