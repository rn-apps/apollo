import { HttpClient } from '@angular/common/http';
import {
  ChangeDetectionStrategy,
  Component,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { RouterModule } from '@angular/router';
import { RnfButton } from '@rn-forge/ng-tailwind';

export type ApiState = 'connecting' | 'connected' | 'unavailable';

/** The Apollo home: brand plus whether the API's liveness probe answers. */
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [RouterModule, RnfButton],
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App implements OnInit {
  protected readonly state = signal<ApiState>('connecting');
  private readonly http = inject(HttpClient);

  ngOnInit(): void {
    this.check();
  }

  protected retry(): void {
    this.check();
  }

  private check(): void {
    this.state.set('connecting');
    this.http.get<{ status?: unknown }>('/livez').subscribe({
      next: (body) =>
        this.state.set(body?.status === 'pass' ? 'connected' : 'unavailable'),
      error: () => this.state.set('unavailable'),
    });
  }
}
