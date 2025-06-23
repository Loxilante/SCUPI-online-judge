/* eslint-disable */
import { viewImage } from "@/service/api";

type Model = {
  title: string;
  content_problem: any;
  score: any;
  type: string;
  stem: string;
  response_limit: any;
  non_programming_answer: string;
};
const mapping = [
  'A',
  'B',
  'C',
  'D',
  'E',
  'F',
  'G',
  'H',
  'I',
  'J',
  'K'
]

export const useResolve = ()=>{
  const resolveContentProblem = (type: string, content_problem: any,stem:any) => {
    let content_problemStr = `<-&^stem${stem}stem$`;
    let non_programming_answerStr = '';
    if (type === 'programming') {
      // content_problem.forEach((item: any) => {
      //   content_problemStr += item.question;
      // });
      content_problemStr += '&->';
      return {
        content_problem: content_problemStr,
        non_programming_answer: non_programming_answerStr
      };
    } else if (type === 'text') {
      content_problem.forEach((item: any, index: number) => {
        content_problemStr += item.question + (index === content_problem.length - 1 ? '' : '|');
        non_programming_answerStr += `<-&${item.answer}&->${index === content_problem.length - 1 ? '' : '|'}`;
      });
      content_problemStr += '&->';
      return {
        content_problem: content_problemStr,
        non_programming_answer: non_programming_answerStr
      };
    }else if(type == 'choice'){
      content_problem.forEach((item: any, index: number) => {
        content_problemStr += item.question + (index === content_problem.length - 1 ? '' : '|');
        non_programming_answerStr += `<-&${item.checked ? item.question : 'incorrect'}&->${index === content_problem.length - 1 ? '' : '|'}`;
      });
      content_problemStr += '&->';
      return {
        content_problem: content_problemStr,
        non_programming_answer: non_programming_answerStr
      };
    }
    return {
      content_problem: content_problemStr,
      non_programming_answer: non_programming_answerStr
    };
  };
  function createDefaultModel(): Model {
    return {
      title: '',
      content_problem: [],
      score: '',
      type: 'text',
      stem: '',
      response_limit: '',
      non_programming_answer: ''
    };
  }
  const handleProblemDetail = (item:any)=>{
    if (!item) return {};
    const reg = /(\^stem)([\s\S]*)(stem\$)/gi;
    const modelDef = { ...item };
    Object.keys(modelDef).forEach(key => {
      if (key === 'content_problem') {
        const content = item[key].replace(reg, '').replace('<-&', '').replace('&->', '');
        const non_programming_answerStr = (item.non_programming_answer || "")
          .replaceAll('<-&', '')
          .replaceAll('&->', '');
        const matchStem = item[key].match(reg);
        let stem = '';
        if (matchStem && matchStem.length > 0) {
          stem = matchStem[0].replace('^stem', '').replace('stem$', '');
          modelDef.stem = stem;
        }
        if (item.type === 'programming') {
          modelDef[key] = [
            {
              question: content,
              type: 'java'
            }
          ];
        } else {
          const arr = content.split('|');
          const non_programming_answerArr = non_programming_answerStr.split('|');
          const result: any = [];
          arr.forEach((arr_item: any, index: number) => {
            if(item.type == 'text'){
              result.push({
                question: arr_item,
                answer: non_programming_answerArr[index] || ""
              });
            }else{
              result.push({
                question: arr_item,
                checked: non_programming_answerArr[index] == arr_item
              });
            }
          });
          modelDef[key] = result;
        }
      } else if (key !== 'stem' && key !== 'non_programming_answer') {
        modelDef[key] = item[key];
      }
    });
    return modelDef
  }
  const handleCommissionDetail = (item:any)=>{
    const modelDef: any = createDefaultModel();
    return modelDef
  }
  const getImageList = async ({course_name, homework_name, id}:{course_name:any,homework_name:any,id:any})=>{
    let res = await viewImage(course_name, homework_name, id)
    let imageList = res.data.map((item: any) => ({
      file: `https://ojapi.loxilante.uno/${item.image}`,
      name: item.name,
      id: item.id,
      status: 'finished'
    }));
    return imageList
  }
  return {
    resolveContentProblem,
    handleCommissionDetail,
    mapping,
    getImageList,
    handleProblemDetail
  }
}
