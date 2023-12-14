import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatButtonModule } from '@angular/material/button';
import { NavComponent } from './nav/nav.component';
import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { HomeComponent } from './home/home.component';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatCardModule } from '@angular/material/card';
import { MatMenuModule } from '@angular/material/menu';
import { DfilesComponent } from './dfiles/dfiles.component';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatRadioModule } from '@angular/material/radio';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { FormsModule,ReactiveFormsModule } from '@angular/forms';
import { MayaComponent } from './maya/maya.component';
import {MatTabsModule} from '@angular/material/tabs';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatSlideToggleModule} from '@angular/material/slide-toggle'
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatDatepickerModule} from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { DrawComponent } from './draw/draw.component';
import { DapiComponent } from './dapi/dapi.component';
import { HttpClientModule } from '@angular/common/http';
import {MatTableModule} from '@angular/material/table';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatBadgeModule} from '@angular/material/badge';
import { TextaiComponent } from './textai/textai.component';
import { DatePipe } from '@angular/common';
import {NgxPrintModule} from 'ngx-print';
import { DqueryComponent } from './dquery/dquery.component';
import { MatDialogModule } from '@angular/material/dialog';
import { ScheduleDialogComponent } from './schedule-dialog/schedule-dialog.component';
import { AiServiceV1Component } from './ai-service-v1/ai-service-v1.component';
import { MatChipsModule } from '@angular/material/chips';
import { ManageControlComponent } from './manage-control/manage-control.component';
import { LogsScreenComponent } from './logs-screen/logs-screen.component';
import { SummerizeComponent } from './summerize/summerize.component';
import { TestingUiComponent } from './testing-ui/testing-ui.component';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatPaginatorModule } from '@angular/material/paginator';
import { OecdComponent } from './oecd/oecd.component';
import { PrettyPipePipe } from './Pipes/pretty-pipe.pipe';
import { UserRequestsComponent } from './user-requests/user-requests.component';

@NgModule({
    declarations: [
        AppComponent,
        NavComponent,
        HomeComponent,
        DfilesComponent,
        MayaComponent,
        DrawComponent,
        DapiComponent,
        TextaiComponent,
        DqueryComponent,
        ScheduleDialogComponent,
        AiServiceV1Component,
        ManageControlComponent,
        LogsScreenComponent,
        SummerizeComponent,
        TestingUiComponent,
        OecdComponent,
        PrettyPipePipe,
        UserRequestsComponent
    ],
    imports: [
        BrowserModule,
        MatPaginatorModule,
        MatButtonToggleModule,
        AppRoutingModule,
        BrowserAnimationsModule,
        MatButtonModule,
        LayoutModule,
        MatToolbarModule,
        MatSidenavModule,
        MatIconModule,
        MatListModule,
        MatGridListModule,
        MatCardModule,
        MatMenuModule,
        MatInputModule,
        MatSelectModule,
        MatSnackBarModule,
        MatRadioModule,
        MatTableModule,
        MatProgressBarModule,
        MatProgressSpinnerModule,
        ReactiveFormsModule,
        FormsModule,
        MatTabsModule,
        MatDatepickerModule,
        MatNativeDateModule,
        HttpClientModule,
        MatBadgeModule,
        NgxPrintModule,
        MatExpansionModule,
        MatSlideToggleModule,
        MatCheckboxModule,
        MatDialogModule,
        MatChipsModule,
        MatButtonToggleModule,
        MatPaginatorModule
    ],
    providers: [DatePipe],
    bootstrap: [AppComponent]
})
export class AppModule { }
