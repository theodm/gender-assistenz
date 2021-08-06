<script>
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";

  import { EditorView } from "@codemirror/view";
  import { EditorState } from "@codemirror/state";

  let classes = '';

  export { classes as class }

  let element: any;
  let editor: any;

  const options = {}

  onMount(() => {
    createEditor(options);
  });

  $: if (element) {
    createEditor(options);
  }

  function createEditor(options: any) {
    if (editor) element.innerHTML = "";

    editor = new EditorView({
        state: EditorState.create({doc: "hello"}),
        parent: element
    });


    // editor.on("cursorActivity", (event) => {
    //   dispatch("activity", event);
    // });
    // editor.on("change", (event) => {
    //   dispatch("change", event);
    // });
    // More events could be set up here
  }
</script>

<div bind:this={element} class={classes} />

<style>
    :global(.cm-editor) {
        height: 100%;
    }
</style>
