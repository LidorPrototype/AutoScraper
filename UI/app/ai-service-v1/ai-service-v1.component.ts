import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { UntypedFormBuilder } from '@angular/forms';
import { COMMA, ENTER, P } from '@angular/cdk/keycodes';
import { MatChipInputEvent } from '@angular/material/chips';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-ai-service-v1',
  templateUrl: './ai-service-v1.component.html',
  styleUrls: ['./ai-service-v1.component.css']
})

export class AiServiceV1Component implements OnInit {
  loaded = false;
  searched = false;
  @ViewChild('fileInput') fileInput: ElementRef | any;
  fileAttr = 'Select PDF File';
  fileselected?: Blob;
  base64: string = '';
  parsing: string = '';
  addOnBlur = true;
  readonly separatorKeysCodes = [ENTER, COMMA] as const;
  resultText: any = null;
  errorText1: any = null;
  errorText2: any = null;
  sentiment: any = null;
  errorSentiment: any = null;
  errorEntities: any = null;
  errorSummary: any = null;
  gotSentiment = true;
  gotEntities = true;
  gotSummary = true;
  entities: any = null;
  pagging = null;
  pages = null;
  contents = null;
  titles = null;
  aiFeature = this._formBuilder.group({
    summary: false,
    ner: false,
    sent: false,
  });
  summary: any = { textType: '', textarea: '', sentiment: [] };
  score!: [
    sentiment: string,
    score: number
  ];

  constructor(private _formBuilder: UntypedFormBuilder, private http: HttpClient, private sant: DomSanitizer) { }

  ngOnInit(): void { }

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();
    // Clear the input value
    event.chipInput!.clear();
  }

  onSelectNewFile(files: any): void {
    this.fileselected = files.target.files[0];
    this.fileAttr = files.target.files[0].name
    this.base64 = 'base64...';
    this.parsing = 'Pages';
  }

  sendFile() {
    let _error = "There was a problem parsing your file, if this error persists, send the other side to the support team:";
    if (this.pagging != null) {
      this.parsing = this.pagging
    }
    this.loaded = false;
    this.searched = true;
    let freader = new FileReader();
    freader.readAsDataURL(this.fileselected as Blob);
    freader.onloadend = () => {
      this.base64 = freader.result as string;
      const url = "https://<INSERT DOMAIN NAME>.azurewebsites.net/api/pdfExtractor";
      let headers = new HttpHeaders();
      let data = { 'name': this.base64.split(',')[1], 'parsing': this.parsing };
      headers.append('Accept', 'application/json');
      let options = { headers: headers };
      this.http.post(url, data, { headers, responseType: 'text' }).subscribe(data => {
        try {
          this.resultText = JSON.parse(data);
          const mapped = Object.keys(this.resultText).map(key => ({ type: key, value: this.resultText[key] }));
          this.resultText = mapped
          console.log("resultText: ", this.resultText);
          this.loaded = true;
        } catch (error) {
          console.log(error);
          const err = error as HttpErrorResponse;
          this.errorText1 = _error;
          this.errorText2 = err;
          this.loaded = false;
        }
      }, error => {
        console.log(error);
        const err = error as HttpErrorResponse;
        this.errorText1 = _error;
        this.errorText2 = err.message;
        this.loaded = false;
      });
    } 
  }

  GetSummary(textarea: string, textType: string) {
    try {
      let headers = new HttpHeaders();
      headers.append('Accept', 'text/html');
      let options = { headers: headers };
      this.gotSummary = false;
      this.http.post('https://<INSERT DOMAIN NAME>.azurewebsites.net/api/summarizeText', { text: textarea }, { headers, responseType: 'text' }).subscribe(data => {
        console.log(data);
        this.summary.textarea = data;
        this.summary.textType = textType;
        this.gotSummary = true;
        this.errorSummary = null;
      });
    } catch (error) {
      console.log(error);
      const err = error as HttpErrorResponse;
      this.errorSummary = err.message;
    }
  }

  GetNER(textarea: string, textType: string) {
    try {
      let headers = new HttpHeaders();
      headers.append('Accept', 'text/html');
      let options = { headers: headers };
      this.gotEntities = false;
      this.http.post('https://<INSERT DOMAIN NAME>.azurewebsites.net/api/ner', { text: textarea }, { headers, responseType: 'text' }).subscribe(data => {
        this.errorEntities = null;
        console.log(data);
        this.entities = JSON.parse(data);
        const mapped = Object.keys(this.entities).map(key => ({ type: key, value: this.entities[key] }));
        this.entities = mapped;
        console.log(this.entities);
        this.gotEntities = true;
      });
    } catch (error) {
      const err = error as HttpErrorResponse;
      console.log(error);
      this.errorEntities = err.message;
    }
  }

  GetSentiment(textarea: string, textType: string) {
    try {
      let headers = new HttpHeaders();
      headers.append('Accept', 'text/html');
      let options = { headers: headers };
      this.gotSentiment = false;
      this.http.post('https://<INSERT DOMAIN NAME>.azurewebsites.net/api/sentiment', { text: textarea }, { headers }).subscribe(data => {
        console.log(data);
        this.sentiment = data;
        this.score = this.sentiment;
        console.log(this.sentiment);
        this.gotSentiment = true;
        this.errorSentiment = null;
      });
    } catch (error) {
      const err = error as HttpErrorResponse;
      console.log(error);
      this.gotSentiment = true;
      this.errorSentiment = err.message
    }
  }

}


