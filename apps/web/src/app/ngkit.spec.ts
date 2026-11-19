import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { RnfButton } from '@rn-forge/ng-tailwind';

@Component({
  imports: [RnfButton],
  template: '<button rnfButton type="button" variant="primary">Open</button>',
})
class NgkitTestHost {}

describe('ngkit', () => {
  it('S2.1.1: tokens load', () => {
    const fixture = TestBed.createComponent(NgkitTestHost);
    fixture.detectChanges();

    const host = fixture.nativeElement as HTMLElement;
    const button = host.querySelector('button.rnf-button');
    expect(button?.textContent).toBe('Open');
    expect(button?.getAttribute('data-variant')).toBe('primary');
  });
});
