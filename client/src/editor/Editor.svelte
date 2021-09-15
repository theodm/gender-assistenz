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
        doc: "Das ist ein Test!",
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
