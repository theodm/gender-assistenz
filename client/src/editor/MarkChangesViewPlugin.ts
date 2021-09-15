import { StateEffect } from "@codemirror/state";
import {
  Decoration,
  DecorationSet,
  EditorView,
  PluginSpec,
  ViewPlugin,
  ViewUpdate,
} from "@codemirror/view";
import type { RangeSet, RangeValue, Range, RangeSetBuilder } from '@codemirror/rangeset';
import type { PossibleCorrection } from "./MarkInfoOccurencesViewPlugin";

export const STATE_EFFECT_SET_POSSIBLE_CORRECTION_PREVIEW =
  StateEffect.define<PossibleCorrection | null>();

class MarkChangesViewPluginClass {
  public currentDecorations: DecorationSet = Decoration.none;

  constructor(public readonly view: EditorView) {}

  update(update: ViewUpdate) {
    for (let transaction of update.transactions) {
      for (let effect of transaction.effects) {
        if (effect.is(STATE_EFFECT_SET_POSSIBLE_CORRECTION_PREVIEW)) {
          const markDecorations: Range<Decoration>[] = [];
          
          if (!effect.value) {
              this.currentDecorations = Decoration.none;
              continue
          }

          for (const change of effect.value?.changes!) {
              function selectClass(type: "NOUN" | "CONJ" | "DET" | "VERB" | "ADJ" | "PRON") {
                switch(type) {
                    case "NOUN":
                        return "change-info-noun"
                    case "VERB":
                        return "change-info-verb"
                    case "DET":
                        return "change-info-art"
                    case "CONJ":
                        return "change-info-conj"
                    case "ADJ":
                        return "change-info-adj"
                    case "PRON":
                        return "change-info-pron_art"
                }
              }
            let markDecoration = Decoration.mark({
              attributes: {
                class: selectClass(change.type)
              },
            });

            markDecorations.push(
              markDecoration.range(
                change._range?.iter()!.from!,
                change._range?.iter().to
              )
            );
          }

          markDecorations.sort((a, b) => a.from - b.from)

          this.currentDecorations = Decoration.none.update({
            add: markDecorations,
            sort: true
          });
        }
      }
    }
  }

  destroy() {}
}

export const MARK_CHANGES_THEME = EditorView.baseTheme({
    ".change-info-default": {
      backgroundColor: "#000000",
    },

    // NOUN
    ".change-info-noun": {
        textDecoration: "underline 2px #60A5FA",
        backgroundColor: "#DBEAFE",
    },

    // CONJ
    ".change-info-conj": {
        textDecoration: "underline 2px #60A5FA",
        backgroundColor: "#DBEAFE",
    },

    // DET
    ".change-info-det": {
        textDecoration: "underline 2px #9CA3AF",
        backgroundColor: "#F3F4F6",        
    },

    // VERB
    ".change-info-verb": {
        textDecoration: "underline 2px #EB5757",
        backgroundColor: "#FDEEEE",
    } ,

    // ADJ
    ".change-info-adj": {
      textDecoration: "underline 2px #F2B24C",
      backgroundColor: "#FEF7ED",
  },
  
    // PRON
    ".change-info-pron": {
      textDecoration: "underline 2px #9CA3AF",
      backgroundColor: "#F3F4F6",    
  }
  
  });

export const MarkChangesViewPlugin = ViewPlugin.fromClass(
  MarkChangesViewPluginClass,
  {
    decorations: (plugin: MarkChangesViewPluginClass) => {
      return plugin.currentDecorations;
    },
  } as PluginSpec<MarkChangesViewPluginClass>
);
