import { Component, OnInit, ChangeDetectorRef, OnDestroy } from '@angular/core';
import { GoogleAuthService } from 'src/app/auth/google-auth.service';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-google-auth',
  templateUrl: './google-auth.component.html',
  styleUrls: ['./google-auth.component.scss'],
})
export class GoogleAuthComponent implements OnInit, OnDestroy {
  isSignedIn: boolean;
  ngUnsubscribe = new Subject<void>();
  constructor(
    private googleAuthService: GoogleAuthService,
    private cd: ChangeDetectorRef,
  ) {
    this.isSignedIn = false;
  }

  ngOnInit(): void {
    this.googleAuthService.initGoogleAuth();
    this.googleAuthService.isSignedIn$
      .pipe(takeUntil(this.ngUnsubscribe))
      .subscribe((isSignedIn) => {
        if (isSignedIn !== this.isSignedIn) {               
          this.isSignedIn = isSignedIn;          
          this.cd.detectChanges();
          if (!this.isSignedIn) window.open("/", "_self");
        }
      });
  }

  signout(): void {
    return this.googleAuthService.signout();
  }

  ngOnDestroy(): void {
    this.ngUnsubscribe.next();
    this.ngUnsubscribe.complete();
  }
}
