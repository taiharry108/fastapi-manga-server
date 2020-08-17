import { Injectable } from '@angular/core';
import { from, Subject } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class GoogleAuthService {
  private _gapiSetup = false;
  private _authInstance: gapi.auth2.GoogleAuth;
  private _error: string;
  private _user: gapi.auth2.GoogleUser;
  isSignedIn$ = new Subject<boolean>();
  constructor() {}
  initGoogleAuth(): void {
    gapi.load('auth2', () => {
      from(
        gapi.auth2.init({
          client_id: environment.googleClientId,
        })
      ).subscribe((auth) => {
            this._gapiSetup = true;
            this._authInstance = auth;
            this.isSignedIn$.next(auth.isSignedIn.get());
            auth.isSignedIn.listen((signedIn) => {              
              this.isSignedIn$.next(signedIn);
              if (signedIn) {
                const id_token = auth.currentUser.get().getAuthResponse().id_token;      
                
                console.log(id_token, auth.currentUser.get().getBasicProfile().getFamilyName());
              }
            });
          });
    });
  }

  signout(): void {
    from(this._authInstance.signOut()).subscribe(
      () => console.log('signout')
    );
  }
}
