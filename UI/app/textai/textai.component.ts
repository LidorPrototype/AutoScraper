import { Component, ElementRef, OnInit, ViewChild  } from '@angular/core';
import { map } from 'rxjs/operators';
import { Breakpoints, BreakpointObserver } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { HttpClient,HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-textai',
  templateUrl: './textai.component.html',
  styleUrls: ['./textai.component.css']
})
export class TextaiComponent {
  /** Based on the screen size, switch from standard to one column per row */
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

  cards = this.breakpointObserver.observe(Breakpoints.Handset).pipe(
    map(({ matches }) => {
      if (matches) {
        return [
          { title: 'Card 1', cols: 1, rows: 1 },
          { title: 'Card 2', cols: 1, rows: 1 },
          { title: 'Card 3', cols: 1, rows: 1 },
          { title: 'Card 4', cols: 1, rows: 1 }
        ];
      }
      return [
        { title: 'Card 1', cols: 2, rows: 1 },
        { title: 'Card 2', cols: 1, rows: 1 },
        { title: 'Card 3', cols: 1, rows: 2 },
        { title: 'Card 4', cols: 1, rows: 1 }
      ];
    })
  );
  apiEndPoint: any;

  constructor(private breakpointObserver: BreakpointObserver,private http: HttpClient) {}
  
  @ViewChild('fileInput') fileInput: ElementRef | any;
  fileAttr = 'Choose File';
  formData:FormData = new FormData();
  uploadFileEvt(pdfFile: any) {
    if (pdfFile.target.files && pdfFile.target.files[0]) {
      this.fileAttr = '';
      Array.from(pdfFile.target.files).forEach((file: any) => {
        this.fileAttr += file.name + '\n';
      });
      //file Save
      let file: File = pdfFile.target.files[0];
      
      this.formData.append('_file', file, file.name);
      // HTML5 FileReader API
      let reader = new FileReader();
      reader.onload = (e: any) => {
        let image = new Image();
        image.src = e.target.result;
        image.onload = (rs) => {
          let imgBase64Path = e.target.result;
        };
      };
      reader.readAsDataURL(pdfFile.target.files[0]);
      // Reset if duplicate image uploaded again
      this.fileInput.nativeElement.value = '';
    } else {
      this.fileAttr = 'Choose File';
    }
  }
  resultText = "";
  sendfileToserver(){
    const url = "https://<INSERT DOMAIN NAME>.azurewebsites.net/post_pdf_file/?example=N";
    let headers = new HttpHeaders();
      /** In Angular 5, including the header Content-Type can invalidate your request */
      headers.append('Content-Type', 'multipart/form-data');
      headers.append('Accept', 'application/json');
      let options = { headers: headers };
      this.http.post(url, this.formData, options)
          .subscribe(
              data => {
                console.log(data);
                this.resultText = data.toString();
              }
          )
  }

}
