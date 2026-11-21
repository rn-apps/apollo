import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { App } from './app';

describe('App', () => {
  let http: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  const root = (fixture: ComponentFixture<App>) =>
    fixture.nativeElement as HTMLElement;
  const status = (fixture: ComponentFixture<App>) =>
    root(fixture)
      .querySelector('[data-testid="api-status"]')
      ?.textContent?.trim();
  const retryButton = (fixture: ComponentFixture<App>) =>
    root(fixture).querySelector('[data-testid="retry"]');
  const expectLivez = () => {
    const req = http.expectOne('/livez');
    expect(req.request.method).toBe('GET');
    return req;
  };

  it('S2.7.1: shows the Apollo brand', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expectLivez().flush({ status: 'pass' });
    await fixture.whenStable();
    expect(root(fixture).querySelector('h1')?.textContent?.trim()).toBe(
      'Apollo',
    );
    expect(root(fixture).querySelector('img')?.getAttribute('src')).toBe(
      'icon.svg',
    );
  });

  it('S2.7.1: reflects API reachability — Connecting before the response', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const req = expectLivez();
    expect(status(fixture)).toBe('Connecting…');
    expect(retryButton(fixture)).toBeNull();
    req.flush({ status: 'pass' });
    await fixture.whenStable();
  });

  it('S2.7.1: reflects API reachability — connected on 200 pass', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expectLivez().flush({ status: 'pass' });
    await fixture.whenStable();
    expect(status(fixture)).toBe('API connected');
    expect(retryButton(fixture)).toBeNull();
  });

  it('S2.7.1: reflects API reachability — unavailable on a request failure', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expectLivez().error(new ProgressEvent('error'));
    await fixture.whenStable();
    expect(status(fixture)).toBe('API unavailable');
    const retry = retryButton(fixture);
    expect(retry).not.toBeNull();
    expect(retry?.classList.contains('rnf-button')).toBe(true);
    expect(retry?.getAttribute('data-variant')).toBe('primary');
  });

  it('S2.7.1: reflects API reachability — unavailable on a 503', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expectLivez().flush(
      { status: 'fail' },
      { status: 503, statusText: 'Service Unavailable' },
    );
    await fixture.whenStable();
    expect(status(fixture)).toBe('API unavailable');
  });

  it('S2.7.1: reflects API reachability — unavailable on an unexpected payload', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expectLivez().flush({ status: 'ok' });
    await fixture.whenStable();
    expect(status(fixture)).toBe('API unavailable');
  });

  it('S2.7.1: reflects API reachability — Retry recovers', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expectLivez().error(new ProgressEvent('error'));
    await fixture.whenStable();
    (retryButton(fixture) as HTMLButtonElement).click();
    fixture.detectChanges();
    await fixture.whenStable();
    expect(status(fixture)).toBe('Connecting…');
    expectLivez().flush({ status: 'pass' });
    await fixture.whenStable();
    expect(status(fixture)).toBe('API connected');
    expect(retryButton(fixture)).toBeNull();
  });
});
