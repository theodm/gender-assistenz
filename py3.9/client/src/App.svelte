<script lang="typescript">
  import { onMount } from "svelte";
  import axios from "axios";
  import { text } from "svelte/internal";
  import Editor from "./editor/Editor.svelte";

  let debounceTimer: any;
  let currentInput: string;

  const debounce = (fn: () => void, timeout: number) => {
    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(fn, timeout);
  };

  async function do_correction(text: string) {
    const result = (
      await axios.post("http://localhost:8080/do_correction", text)
    ).data;

    console.log(result);
  }

  function onInputChanged(newInput: string) {
    currentInput = newInput;

    debounce(() => {
      do_correction(newInput);
    }, 200);
  }

  // type HanTaResult = [string, string, string[], string];

  // let currentTokens: HanTaResult[] = [["Test", "", [], "ADV"]];

  // onMount(() => {
  //   tokenize();
  // });

  // function generateSentences(currentTokens: HanTaResult[]) {
  //   console.log("generate sentences");

  //   const sentences: HanTaResult[][] = [];
  //   let currentSentence: HanTaResult[] = [];
  //   for (let i = 0; i < currentTokens.length; i++) {
  //     const c = currentTokens[i];

  //     currentSentence.push(currentTokens[i]);

  //     if (c[0] == ".") {
  //       sentences.push(currentSentence);
  //       currentSentence = [];

  //       continue;
  //     }
  //   }

  // if (currentSentence.length > 0) {
  // 	sentences.push(currentSentence);
  // }

  // console.log(sentences)
  //   return sentences;
  // }
</script>

<div class="flex w-full h-screen">
  <div class="w-full p-4 bg-red-400">
    <h1 class="mb-2">Eingabe:</h1>
    <div class="">
      <Editor class="w-full p-2 h-96" />
      <!-- <textarea class="w-full p-2 h-96" on:input={(e) => onInputChanged(e.target.value)}/> -->
    </div>
  </div>
  <div class="w-full p-4 bg-blue-400 ">
    <h1 class="mb-2">Ausgabe:</h1>
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
  }
</style>
