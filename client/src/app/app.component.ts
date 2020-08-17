import { Component, OnInit } from '@angular/core';
import { GoogleAuthService } from './auth/google-auth.service';
declare var $: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'client';
}
