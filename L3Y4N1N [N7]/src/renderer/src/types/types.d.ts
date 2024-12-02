import { Question } from "src/types/types"

interface VideoPLayerProps {
  videoStreamlink: string
  linkType?: LinkType
}

interface QuestionComponentProp {
  question: Question
}

export type { VideoPLayerProps, QuestionComponentProp }
