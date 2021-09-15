import { ChangeDesc, MapMode, StateEffect } from "@codemirror/state";
import {
  Decoration,
  DecorationSet,
  EditorView,
  PluginSpec,
  ViewPlugin,
  ViewUpdate
} from "@codemirror/view";
import { RangeSet, RangeValue, Range, RangeSetBuilder } from '@codemirror/rangeset';
import { STATE_EFFECT_SHOW_TOOLTIP_INFO } from "./InfoOccurencesTooltipField";

export interface Change {
  from: number;
  to: number;
  type: "NOUN" | "CONJ" | "DET" | "VERB" | "ADJ";
  replace_with: string;
  
  _range: RangeSet<RangeValue> | undefined;
}

export type PossibleCorrection = {
  type: "BOTH_FORMS" | "*" | "PLURAL_*";
  changes: Change[];
};

export interface InfoOccurence {
  from: number;
  to: number;

  shouldBeGendered: boolean;
  reasonNotGendered: string[][];
  possibleCorrections: PossibleCorrection[]

  _range: RangeSet<RangeValue> | undefined;
  _id: number;
}

function createRangeForInfoOcurrence(
  infoOccurence: InfoOccurence
) {
  // Womöglich ineffizient :/
  const rangeSet = new RangeSetBuilder();

  rangeSet.add(infoOccurence.from, infoOccurence.to, new DummyRangeValue("value"));

  infoOccurence._range = rangeSet.finish();

  if (!infoOccurence.possibleCorrections)
    return;

  for (const possibleCorrection of infoOccurence.possibleCorrections) {
      for (const change of possibleCorrection.changes) {
        const rangeSet = new RangeSetBuilder();

        rangeSet.add(change.from, change.to, new DummyRangeValue("value"));

        change._range = rangeSet.finish();
      }
  }
}

function updateRangeForInfoOccurence(
  infoOccurence: InfoOccurence,
  changeDesc: ChangeDesc
) {
  infoOccurence._range = infoOccurence._range?.map(changeDesc)

  if (!infoOccurence.possibleCorrections)
    return;

  for (const possibleCorrection of infoOccurence.possibleCorrections) {
    for (const change of possibleCorrection.changes) {
      change._range = change._range?.map(changeDesc)
    }
  }

}

export const STATE_EFFECT_REPLACE_INFOS = StateEffect.define<InfoOccurence[]>();
export const STATE_EFFECT_REMOVE_INFO = StateEffect.define<InfoOccurence>();

export const STATE_EFFECT_SET_SHOW_DEBUGGING_INFO = StateEffect.define<boolean>();

export const STATE_EFFECT_TEMP_HIDE_INFO = StateEffect.define<void>();
export const STATE_EFFECT_TEMP_SHOW_INFO = StateEffect.define<void>();

class DummyRangeValue extends RangeValue {
  value: string;

  constructor(value: string) {
    super();
    this.value = value;
  }

  startSide = 100000000;
  endSide = -100000000;
  mapMode = MapMode.TrackDel;

  eq(other: DummyRangeValue) {
    return this.value === other.value;
  }
}

class MarkInfoOccurencesViewPluginClass {
  public infoOccurences: Array<InfoOccurence> = [];
  public infoOccurencesRanges: DecorationSet = Decoration.none;

  public infoOccurencesIDCounter: number = 1
  private showDebuggingInfo = false;

  constructor(public readonly view: EditorView) {}

  private rebuildDecorationSet() {
    const markDecorations: Range<Decoration>[] = []

    let idCounter = 1

    for (const infoOccurence of this.infoOccurences) {
      infoOccurence._id = idCounter++;

      if (!this.showDebuggingInfo && !infoOccurence.shouldBeGendered) {
        continue
      }

      let markDecoration = Decoration.mark({
        infoOccurence: infoOccurence,
        attributes: {
          class: `cm-info-occurence ${infoOccurence.shouldBeGendered ? 'cm-info-occurence-correction' : 'cm-info-occurence-no-correction'}`,
          "data-index": "" + infoOccurence._id,
        },
      });   

      markDecorations.push(markDecoration.range(infoOccurence._range?.iter()!.from!, infoOccurence._range?.iter().to))
    }

    this.infoOccurencesRanges = Decoration.none.update({
      add: markDecorations,
      sort: true
    });
  }

  update(update: ViewUpdate) {
    for (let transaction of update.transactions) {
      for (let effect of transaction.effects) {
        if (effect.is(STATE_EFFECT_SET_SHOW_DEBUGGING_INFO)) {
          this.showDebuggingInfo = effect.value;

          this.rebuildDecorationSet();
        }

        if (effect.is(STATE_EFFECT_REMOVE_INFO)) {
          this.infoOccurences = this.infoOccurences.filter(it => it !== effect.value);

          this.infoOccurencesRanges = this.infoOccurencesRanges.update({
            filter: (from, to, value) => {
              return value.spec.infoOccurence !== effect.value
            }
          })
        }

        if (effect.is(STATE_EFFECT_TEMP_HIDE_INFO)) {
          this.infoOccurencesRanges = this.infoOccurencesRanges.update({
            filter: (from, to, value) => {
              return false;
            }
          })
        }

        if (effect.is(STATE_EFFECT_TEMP_SHOW_INFO)) {
          this.rebuildDecorationSet();
        }

        if (effect.is(STATE_EFFECT_REPLACE_INFOS)) {
          this.infoOccurences = [...effect.value];

          for (const infoOccurence of effect.value) {            
            createRangeForInfoOcurrence(infoOccurence);
          }

          this.rebuildDecorationSet();
        }
      }
    }

    this.infoOccurencesRanges = this.infoOccurencesRanges.map(update.changes);
    this.infoOccurences.forEach(it => updateRangeForInfoOccurence(it, update.changes));
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

        const occurenceIDStr = target.dataset["index"];

        if (!occurenceIDStr) {
          return;
        }

        const occurenceID = Number.parseInt(occurenceIDStr);

        const occurence = this.infoOccurences.find(it => it._id === occurenceID);

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
