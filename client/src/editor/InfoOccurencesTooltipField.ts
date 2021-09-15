import { EditorState, StateEffect, StateField } from "@codemirror/state";
import type { Tooltip } from "@codemirror/tooltip";
import type { InfoOccurence } from "./MarkInfoOccurencesViewPlugin";

import { showTooltip } from "@codemirror/tooltip";

import InfoOccurenceTooltip from "./InfoOccurenceTooltip.svelte";
import type { EditorView } from "@codemirror/view";

export const STATE_EFFECT_SHOW_TOOLTIP_INFO =
  StateEffect.define<InfoOccurence>();

export const STATE_EFFECT_DONT_HIDE_TOOLTIP_INFO = StateEffect.define<void>();


export const InfoOccurencesTooltipField = (
  getEditorView: () => EditorView,
  getConvertIntoGenderFormFn: () => (str: string) => string
) => {
    
  return StateField.define<Tooltip | null>({
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
                  infoOccurence: infoOccurence,
                  editorView: getEditorView(),
                  getConvertIntoGenderFormFn: getConvertIntoGenderFormFn
                },
              });

              return { dom };
            },
          };
        }

        if (effect.is(STATE_EFFECT_DONT_HIDE_TOOLTIP_INFO)) {
          return tooltip;
        }
      }


      // Keine Veränderung
      return null;
    },

    provide: (f) =>
      showTooltip.computeN([f], (state) =>
        state.field(f) == null ? [] : [state.field(f)]
      ),
  });
};
