<script>
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";

  import type {DecorationSet, PluginSpec, ViewUpdate} from "@codemirror/view";
  import {  ViewPlugin } from "@codemirror/view";
  import { EditorView, Decoration, keymap } from "@codemirror/view";
  import { EditorState, StateEffect, Transaction } from "@codemirror/state";

  import type {Tooltip} from "@codemirror/tooltip"
  import {showTooltip} from "@codemirror/tooltip"
  import {StateField} from "@codemirror/state"

  import TooltipTt from "./InfoOccurenceTooltip.svelte";

  import type { InfoOccurence} from "./MarkInfoOccurencesViewPlugin"
  import { STATE_EFFECT_REPLACE_INFOS} from "./MarkInfoOccurencesViewPlugin"
  import { STATE_EFFECT_SET_SHOW_DEBUGGING_INFO } from "./MarkInfoOccurencesViewPlugin"
  import { MarkInfoOccurencesViewPlugin, MARK_INFO_OCCURENCE_THEME} from "./MarkInfoOccurencesViewPlugin";
  import {InfoOccurencesTooltipField} from "./InfoOccurencesTooltipField"
import { MarkChangesViewPlugin, MARK_CHANGES_THEME } from "./MarkChangesViewPlugin";


  let classes = "";
  

  export { classes as class };

  export let convertIntoGenderFormFn: (str: string) => string;

  let lastInfos: InfoOccurence[];
  export let infos: InfoOccurence[];

  export let showDebuggingInfos: boolean;

  let element: any;
  
  const options = {};
  let editor: EditorView | null = null;

  onMount(() => {
    createEditor(options);
  });

  $: if (element) {
    createEditor(options);

    window.getEditorContent = () => {
      return editor?.state.doc.toJSON().join("\n");
    }
  }

  function createEditor(options: any) {
    if (editor) element.innerHTML = "";

    editor = new EditorView({
      state: EditorState.create({
        doc: `##
## Für Präsentationszwecke bitte "Zwischenergebnisse anzeigen" aktivieren.
##

# Toaster ist keine Personenbezeichnung, zugehöriges Pronomen wird erkannt. #
Der Toaster, der kaputt ist, wird repariert. Er war einfach zu reparieren.

# Satz ist bereits geschlechtsneutral formuliert. #
Studentinnen und Studenten werden dazu aufgerufen, ihre Arbeiten abzugeben.

# Generierte Korrektur setzt sich grammatikalisch korrekt in die Konjunktion ein. #
Studenten, Studentinnen und Lehrer werden dazu aufgerufen, die Mensa zu verlassen.

# Auch für Pronomen wird die bestehende Geschlechtsneutralität berücksichtigt. #
Er und Sie gehen ein Eis essen.

# Scholz ist ein Eigenname, das Nomen und das Pronomen erhalten die gleiche Klassifikation. #
Bundeskanzler Scholz hielt eine Rede. Er machte dabei keine Aussagen zur Besetzung des Gesundheitsministeriums.

# Weitere Beispiele im Zusammenhang mit Eigennamen. #
Elon Musk, der Investor, war in Deutschland
Betreiber wird Klesch aus Wiesbaden.

# Beispiele, die korrigiert werden müssen. #
Die Studenten und Dozenten gehen ein Eis essen.

# Auch zusammengesetzte Nomen werden berücksichtigt. #
Die Unterhaltungselektroniktelefonverarbeitungspartner warten auf einen besseren Tag.

# Hier ist der Korrekturvorschlag etwas komplexer aber korrekt. #
Ein Student, dessen Abgabe verstrichen ist, kann den Kurs wiederholen.

# Ein bisschen echter Text. #
Wenn in einem Strafprozeß in Großbritannien der Zeuge der Krone ("Queens evidence") auftritt, muß der Richter die Geschworenen auf die "Gefahren dieses Beweismittels" hinweisen.
Der Kronzeuge - eine "Gefahr" für die Wahrheitsfindung, weil seine Aussage das Ergebnis eines Handels mit dem Ankläger darstellt?
Und dies sogar in dem Rechtssystem, in dem dieser "Zeuge" schon so lange zu Hause ist?
Seit gut zwei Jahren hantiert auch die deutsche Justiz mit dem Instrument, das ihr im Frühjahr 1989 (nach heftigem parlamentarischen Streit und drei vergeblichen Anläufen 1975, 1977 und 1986) an die Hand gegeben wurde.
Ein Gesetz übrigens, dem von Beginn an ein ungewöhnlicher Makel anhaftete:
Es war befristet, versehen mit dem Verfallsdatum Ende 1992, weil seine Schöpfer die eigenen Argumente offenbar nicht allzu hoch einschätzten.
Deshalb muß der Bundestag nach der Sommerpause entscheiden, ob er die Regelung fortschreiben will.
Und es zeichnet sich eine Diskussion über die Frage ab, ob er sich denn "bewährt" hat - dieser "Zeuge der Krone".
Erhofft hatten sich seine Erfinder (an vorderster Front standen damals CSU-Innenminister Friedrich Zimmermann und FDP-Justizressortchef Hans Engelhard) lauter fulminante Ergebnisse.
Der Kronzeuge sollte die terroristische Szene verunsichern, Mitglieder der Rote Armee Fraktion zum Aussteigen animieren, begangene Straftaten aufklären, gesuchte Täter fassen und geplante Morde verhindern helfen.
Fürwahr ein stolzes Sortiment, für das es sich womöglich gelohnt hätte, ein Stück Gleichheit vor dem Recht aufs Spiel zu setzen und demjenigen Strafrabatt zu gewähren, der diese Wundertaten während einer der Strafprozeßordnung folgenden Hauptverhandlung vollbringt, wenn....
Ja, wenn... - aber hat dies ein einziges Mal stattgefunden?`,
        extensions: [
          EditorView.lineWrapping,
           MarkInfoOccurencesViewPlugin, 
           MarkChangesViewPlugin, 
           InfoOccurencesTooltipField(() => editor!, () => convertIntoGenderFormFn), 
           MARK_INFO_OCCURENCE_THEME,
            MARK_CHANGES_THEME,
             EditorView.theme({
          ".cm-tooltip": {
            "border": "none",
            "background-color": "unset"
          }
        })],
      }),
      parent: element,
    });

    const effects: StateEffect<unknown>[] = [
    ];

    editor.dispatch({ effects });


  }
  $: {
    if (editor) {
      {
        if (lastInfos !== infos) {
          const effects: StateEffect<unknown>[] = [
            STATE_EFFECT_REPLACE_INFOS.of(infos)
          ];

          editor.dispatch({ effects });

          lastInfos = infos;
        }
      }
      {
        const effects: StateEffect<unknown>[] = [
          STATE_EFFECT_SET_SHOW_DEBUGGING_INFO.of(showDebuggingInfos)
        ];

        editor.dispatch({ effects });
      }
    }

    
  }

</script>

<div bind:this={element} class={classes} />

<style>
  :global(.cm-editor) {
    height: 100%;
  }

  :global(.cm-editor) {
    background-color: white;
    border: 1px solid black;
  }

  :global(.cm-editor.cm-focused) {
    outline: 0;
  }
</style>
