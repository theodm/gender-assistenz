<script lang="ts">
  import "./global.css";
  import {onMount} from 'svelte'
  import Editor from './editor/Editor.svelte'
  import axios from "axios";
import type { InfoOccurence } from './editor/MarkInfoOccurencesViewPlugin';

  let analyzeResult: null | AnalyzeResult = null;
  let showDebuggingInfos = false;
  let currentGenderForm: "*" | "_" | "I" | ":" = "*";

  interface AnalyzeResult {
    text: string;
    infos: Array<InfoOccurence>;
  }


  const apiBaseUrl = (typeof __SNOWPACK_ENV__ !== 'undefined' && __SNOWPACK_ENV__.MODE === 'development') ? "http://localhost:8080" : ""
  async function analyze(text: string) {
    const result = (
      await axios.post(apiBaseUrl + "/analyze", text)
    ).data;

    console.log(result);

    analyzeResult = result;
  }

  
  async function displacy(text: string) {
    window.open(apiBaseUrl + `/displacy?doc=${text}`,'_blank');
  }

async function tagging(text: string) {
    window.open(apiBaseUrl + `/tagging?doc=${text}`,'_blank');
  }

  function genderFormToConvertFn(genderForm: "*" | "_" | "I" | ":") {
    switch(genderForm) {
      case "*":
        return (str: string) => str.replaceAll("?I", "*i").replaceAll("?", "*");
      case "_":
        return (str: string) => str.replaceAll("?I", "_i").replaceAll("?", "_")
      case "I":
        return (str: string) => str.replaceAll("?I", "I").replaceAll("?", "/")
      case ":":
        return (str: string) => str.replaceAll("?I", ":i").replaceAll("?", ":")

    }
  }
  

</script>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
  }

</style>

<div class="w-full h-screen p-4 App">
  <div class="text-xl text-center">Korrektur-Tool für gendergerechte Sprache</div>

  <div class="flex py-2">
  </div>
  <div class="flex justify-center w-full py-2 align-middle h-5/6">
      <Editor infos={analyzeResult ? analyzeResult.infos : []} showDebuggingInfos={showDebuggingInfos} convertIntoGenderFormFn={genderFormToConvertFn(currentGenderForm)} class="w-full"/>
      <div class="w-4/12 p-3 ml-5 border border-black">
        
        <div class="flex justify-around w-full p-2">
          <button on:click={() => analyze(window.getEditorContent())} class="flex items-center px-4 py-2 font-bold text-white align-middle bg-blue-500 rounded hover:bg-blue-700">
            <!-- <div class="w-2 h-2 mr-2 bg-white"></div> -->
            Überprüfen
          </button>
      </div>
        <div class="mt-5 text-center text-gray-800">Einstellungen</div>
        <div class="">
          <label class="block mt-4">
            <span class="text-xs text-gray-700">Genderform</span>
            <select class="block w-full mt-1" value={currentGenderForm} on:change={(event) => { currentGenderForm = event.target.value }}>
              <option value="*">Gendersternchen (Student*innen)</option>
              <option value="_">Genderunterstrich (Student_innen)</option>
              <option value="I">Binnen-I (StudentInnen)</option>
              <option value=":">Genderdoppelpunkt (Student:innen)</option>
            </select>
          </label>
        </div>
        <div class="mt-5 text-center text-gray-800">Debugging</div>
        <div class="">
          <label class="flex items-center justify-between mt-4 ">
            <span class="text-xs text-gray-700">Zwischenergebnisse anzeigen</span>
            <input type="checkbox" checked={showDebuggingInfos} on:change={(event) => { showDebuggingInfos = event.target.checked }}>
          </label>
          <label class="flex items-center justify-between mt-4 ">
            <span class="text-xs text-gray-700">Abhängigkeiten visualisieren</span>
            
            <button on:click={() => displacy(window.getEditorContent())} class="flex items-center px-4 py-2 text-xs font-bold text-white align-middle bg-gray-500 hover:bg-gray-700">
              DisplacY
            </button>
          </label>
          
          <label class="flex items-center justify-between mt-4 ">
            <span class="text-xs text-gray-700">Tagging visualisieren</span>
            
            <button on:click={() => tagging(window.getEditorContent())} class="flex items-center px-4 py-2 text-xs font-bold text-white align-middle bg-gray-500 hover:bg-gray-700">
              SpacY
            </button>
          </label>

        </div>
      </div>
  </div>
</div>
