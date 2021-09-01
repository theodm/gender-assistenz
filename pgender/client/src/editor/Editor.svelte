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

  import type { InfoOccurence } from "./MarkInfoOccurencesViewPlugin"
  import { MarkInfoOccurencesViewPlugin, MARK_INFO_OCCURENCE_THEME, STATE_EFFECT_ADD_INFO} from "./MarkInfoOccurencesViewPlugin";
  import {InfoOccurencesTooltipField} from "./InfoOccurencesTooltipField"


  let classes = "";

  export { classes as class };

  export let infos: InfoOccurence[];

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
        extensions: [EditorView.lineWrapping, MarkInfoOccurencesViewPlugin, InfoOccurencesTooltipField, MARK_INFO_OCCURENCE_THEME, EditorView.theme({
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
      const effects: StateEffect<unknown>[] = infos.map(it => STATE_EFFECT_ADD_INFO.of(it));

      editor.dispatch({ effects });
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
