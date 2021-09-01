import { StateEffect, StateField } from "@codemirror/state";
import type { Tooltip } from "@codemirror/tooltip";
import type { InfoOccurence } from "./MarkInfoOccurencesViewPlugin";

import {showTooltip} from "@codemirror/tooltip"

import InfoOccurenceTooltip from "./InfoOccurenceTooltip.svelte"

export const STATE_EFFECT_SHOW_TOOLTIP_INFO =
  StateEffect.define<InfoOccurence>();

export const InfoOccurencesTooltipField = StateField.define<Tooltip | null>({
  create: () => null,

  update(tooltip, tr) {
    for (let effect of tr.effects) {
      if (effect.is(STATE_EFFECT_SHOW_TOOLTIP_INFO)) {
        const infoOccurence = effect.value;

        return {
          pos: infoOccurence.from,
          above: true,
          strictSide: true,
          class: "cm-cursor-tooltip",

          create: () => {
            let dom = document.createElement("div");
            
            new InfoOccurenceTooltip({
              target: dom,
              props: {
                infoOccurence: infoOccurence
              }
            });

            return { dom };
          },
        };
      }
    }
    
    return null;
  },

  provide: (f) => showTooltip.computeN([f], (state) => state.field(f) == null ? [] : [state.field(f)]),
});
