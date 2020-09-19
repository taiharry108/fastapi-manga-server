import { Component, OnInit, ChangeDetectorRef, NgZone } from '@angular/core';
import { GoogleAuthService } from 'src/app/auth/google-auth.service';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-nav',
  templateUrl: './user-nav.component.html',
  styleUrls: ['./user-nav.component.scss'],
})
export class UserNavComponent implements OnInit {
  imgUrl$: Observable<string>;
  imgUrl: string;

  constructor(
    private googleAuthService: GoogleAuthService,
    private cd: ChangeDetectorRef,
    private router: Router,
    private zone: NgZone
  ) {}

  ngOnInit(): void {
    this.imgUrl$ = this.googleAuthService.imgUrl$;
    this.imgUrl$.subscribe((imgUrl) => {
      this.imgUrl = imgUrl;
      this.cd.detectChanges();
    });
  }

  signout(): void {
    return this.googleAuthService.signout();
  }

  navigate(page: string): void {
    this.zone.run(() => this.router.navigate([`/${page}`]));
  }
}
