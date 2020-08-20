import { Injectable } from '@angular/core';
import { from, Subject } from 'rxjs';
import { environment } from '../../environments/environment';
import { ApiService } from '../api.service';

@Injectable({
  providedIn: 'root',
})
export class GoogleAuthService {
  private _authInstance: gapi.auth2.GoogleAuth;
  isSignedIn$ = new Subject<boolean>();
  constructor(private api: ApiService) {}
  initGoogleAuth(): void {
    gapi.load('auth2', () => {
      from(
        gapi.auth2.init({
          client_id: environment.googleClientId,
        })
      ).subscribe((auth) => {
            this._authInstance = auth;            
            this.isSignedIn$.next(auth.isSignedIn.get());
            auth.isSignedIn.listen((signedIn) => this.isSignedIn$.next(signedIn));
          });
    });
    this.isSignedIn$.subscribe(signedIn => {   
      if (signedIn)   {
        console.log("hey i'm in!");
        const idToken = this._authInstance.currentUser.get().getAuthResponse().id_token;
        this.api.logInToServer(idToken);
      }
    })
  }

  signout(): void {
    console.log('here');
    from(this._authInstance.signOut()).subscribe(
      () => this.api.logoutFromServer()
    );
  }
}
