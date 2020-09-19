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
  imgUrl$ = new Subject<string>();
  constructor(private api: ApiService) {
    this.isSignedIn$.subscribe(signedIn => {
      if (signedIn) {
        const idToken = this._authInstance.currentUser.get().getAuthResponse().id_token;
        const imgUrl = this._authInstance.currentUser.get().getBasicProfile().getImageUrl();
        this.imgUrl$.next(imgUrl);
        this.api.logInToServer(idToken);
      }
    });
    this.initGoogleAuth();
  }
  initGoogleAuth(): void {
    // gapi.load('auth2', () => {
    //   gapi.auth2.init({client_id: environment.googleClientId}).then(auth =>{
    //     this._authInstance = auth;
    //     this.isSignedIn$.next(auth.isSignedIn.get());
    //     auth.isSignedIn.listen((signedIn) => this.isSignedIn$.next(signedIn));
    //   });
    // });
  }

  signout(): void {
    console.log('here');
    from(this._authInstance.signOut()).subscribe(
      () => this.api.logoutFromServer()
    );
  }
}
