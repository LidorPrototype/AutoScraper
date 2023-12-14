import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DapiComponent } from './dapi/dapi.component';
import { DfilesComponent } from './dfiles/dfiles.component';
import { DqueryComponent } from './dquery/dquery.component';
import { DrawComponent } from './draw/draw.component';
import { HomeComponent } from './home/home.component';
import { MayaComponent } from './maya/maya.component';
import { TextaiComponent } from './textai/textai.component';
import { AiServiceV1Component } from './ai-service-v1/ai-service-v1.component';
import { ManageControlComponent } from './manage-control/manage-control.component'
import { LogsScreenComponent } from './logs-screen/logs-screen.component'
import { UserRequestsComponent } from './user-requests/user-requests.component'
import { SummerizeComponent } from './summerize/summerize.component'
import { TestingUiComponent } from './testing-ui/testing-ui.component';
import { OecdComponent} from './oecd/oecd.component';

const routes: Routes = [
  {path:'',component: HomeComponent},
  {path:'home',component: HomeComponent},
  {path:'dfiles',component: DfilesComponent},
  {path:'maya',component: MayaComponent},
  {path:'draw',component: DrawComponent},
  {path:'dapi',component: DapiComponent},
  {path: 'dquery', component:DqueryComponent},
  {path: 'textai', component:TextaiComponent},
  {path: 'aiservices', component:AiServiceV1Component},
  {path: 'manageControl', component:ManageControlComponent},
  {path: 'logs', component:LogsScreenComponent},
  {path: 'userRequests', component:UserRequestsComponent},
  {path: 'summarize', component:SummerizeComponent},
  {path: 'testing', component:TestingUiComponent},
  {path: 'oecd', component:OecdComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
