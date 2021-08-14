<script>
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";

  import { EditorView, Decoration, DecorationSet, keymap } from "@codemirror/view";
  import { EditorState, StateField, StateEffect } from "@codemirror/state";


  const addUnderline = StateEffect.define<{ from: number; to: number }>();

  const underlineMark = Decoration.mark({ class: "cm-underline" });

  const underlineField = StateField.define<DecorationSet>({
    create() {
      return Decoration.none;
    },
    update(underlines, tr) {
      underlines = underlines.map(tr.changes);
      for (let e of tr.effects)
        if (e.is(addUnderline)) {
          underlines = underlines.update({
            add: [underlineMark.range(e.value.from, e.value.to)],
          });
        }
      return underlines;
    },
    provide: (f) => EditorView.decorations.from(f),
  });

  const underlineTheme = EditorView.baseTheme({
    ".cm-underline": { textDecoration: "underline 3px red" },
  });

  function underlineSelection(view: EditorView) {
    let effects: StateEffect<unknown>[] = view.state.selection.ranges
      .filter((r) => !r.empty)
      .map(({ from, to }) => addUnderline.of({ from, to }));
    if (!effects.length) return false;

    if (!view.state.field(underlineField, false))
      effects.push(
        StateEffect.appendConfig.of([underlineField, underlineTheme])
      );
    view.dispatch({ effects });
    return true;
  }

  const underlineKeymap = keymap.of([
    {
      key: "Mod-h",
      preventDefault: true,
      run: underlineSelection,
    },
  ]);
  let classes = "";

  export { classes as class };

  let element: any;
  let editor: any;

  const options = {};

  onMount(() => {
    createEditor(options);
  });

  $: if (element) {
    createEditor(options);
  }

  function createEditor(options: any) {
    if (editor) element.innerHTML = "";

    editor = new EditorView({
      state: EditorState.create({
        doc: "hello",
        extensions: [underlineKeymap],
      }),
      parent: element,
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

  :global(.cm-editor) {
    background-color: white;
    border: 1px solid black;
  }

  :global(.cm-editor.cm-focused) {
    outline: 0;
  }
</style>
