import { StateEffect } from "@codemirror/state";
import {
  Decoration,
  DecorationSet,
  EditorView,
  PluginSpec,
  ViewPlugin,
  ViewUpdate,
} from "@codemirror/view";
import { STATE_EFFECT_SHOW_TOOLTIP_INFO } from "./InfoOccurencesTooltipField";

export interface InfoOccurence {
  from: number;
  to: number;

  shouldBeGendered: boolean;
  reasonNotGendered: string[][];
}

export const STATE_EFFECT_ADD_INFO = StateEffect.define<InfoOccurence>();

class MarkInfoOccurencesViewPluginClass {
  public readonly infoOccurences: Array<InfoOccurence> = [];
  public infoOccurencesRanges: DecorationSet = Decoration.none;

  constructor(public readonly view: EditorView) {}

  update(update: ViewUpdate) {
    for (let transaction of update.transactions) {
      for (let effect of transaction.effects) {
        if (effect.is(STATE_EFFECT_ADD_INFO)) {
          this.infoOccurences.push(effect.value);

          let markDecoration = Decoration.mark({
            attributes: {
              class: `cm-info-occurence ${effect.value.shouldBeGendered ? 'cm-info-occurence-correction' : 'cm-info-occurence-no-correction'}`,
              "data-index": "" + (this.infoOccurences.length - 1),
            },
          });

          this.infoOccurencesRanges = this.infoOccurencesRanges.update({
            add: [markDecoration.range(effect.value.from, effect.value.to)],
            sort: true
          });
        }
      }
    }

    this.infoOccurencesRanges = this.infoOccurencesRanges.map(update.changes);
  }

  destroy() {}
}

export const MARK_INFO_OCCURENCE_THEME = EditorView.baseTheme({
  ".cm-info-occurence": {
    cursor: "pointer",
  },
  ".cm-info-occurence-no-correction": {
    textDecoration: "underline 2px #9CA3AF",
    backgroundColor: "#F3F4F6",
  },
  ".cm-info-occurence-correction": {
    textDecoration: "underline 2px #60A5FA",
    backgroundColor: "#DBEAFE",
  },


});

export const MarkInfoOccurencesViewPlugin = ViewPlugin.fromClass(
  MarkInfoOccurencesViewPluginClass,
  {
    eventHandlers: {
      click: function (
        this: MarkInfoOccurencesViewPluginClass,
        event: MouseEvent
      ) {
        if (!event.target) {
          return;
        }

        if (!(event.target instanceof HTMLElement)) {
          return;
        }

        const target = event.target;

        if (!target.classList.contains("cm-info-occurence")) {
          return;
        }

        const occurenceIndexStr = target.dataset["index"];

        if (!occurenceIndexStr) {
          return;
        }

        const occurenceIndex = Number.parseInt(occurenceIndexStr);

        const occurence = this.infoOccurences[occurenceIndex];

        if (!occurence) {
          return;
        }

        const effects: StateEffect<unknown>[] = [
          STATE_EFFECT_SHOW_TOOLTIP_INFO.of(occurence),
        ];

        this.view.dispatch({ effects });
      },
    },
    decorations: (plugin: MarkInfoOccurencesViewPluginClass) => {
      return plugin.infoOccurencesRanges;
    },
  } as PluginSpec<MarkInfoOccurencesViewPluginClass>
);
