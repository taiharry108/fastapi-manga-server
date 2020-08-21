import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { GoogleAuthService } from 'src/app/auth/google-auth.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-user-nav',
  templateUrl: './user-nav.component.html',
  styleUrls: ['./user-nav.component.scss']
})
export class UserNavComponent implements OnInit {

  imgUrl$: Observable<string>;
  imgUrl: string;

  constructor(private googleAuthService: GoogleAuthService,
    private cd: ChangeDetectorRef,
    ) { }

  ngOnInit(): void {
    this.imgUrl$ = this.googleAuthService.imgUrl$;
    this.imgUrl$.subscribe(imgUrl => {      
      this.imgUrl = imgUrl;
      this.cd.detectChanges();
    })
  }

  signout(): void {
    return this.googleAuthService.signout();
  }

}
