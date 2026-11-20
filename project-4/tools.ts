import { LogOptions, LogResult, simpleGit, type SimpleGit } from "simple-git";

import { CommitFormat, DiffFormat } from "./types";

let simpleGitInstance: SimpleGit;

const getGitInstance = (
  baseDir: string = process.cwd(),
): SimpleGit => {
  return simpleGitInstance = simpleGit({
    strict: true,
    binary: "git",
    baseDir,
  });
}

export const git_log = async ({
  repoPath,
  file,
  format = CommitFormat.medium,
  from,
  to,
}: {
  repoPath?: string;
  file?: string;
  format?: CommitFormat;
  from?: string;
  to?: string;
}): Promise<string> => {
  const git = getGitInstance(repoPath);

  if(from === undefined && to !== undefined){
    throw new Error("'from' param is required when 'to' is present");
  }

  let options: LogOptions = {};

  if(file !== undefined) options.file = file;
  if(from !== undefined) options.from = from;
  if(to !== undefined) options.to = to;

  const response = await git.log({ ...options, "--pretty": format});

  return "response";
}

export const git_diff = async ({
  repoPath,
  from,
  to,
  staged,
  files,
  format = DiffFormat.patch,
  reverse,
  detectRenames,
  diffFilter,
  exclude = [],
}: {
  repoPath?: string,
  from?: string,
  to?: string,
  staged?: boolean,
  files?: string[]
  format?: DiffFormat,
  reverse?: boolean,
  detectRenames?: boolean,
  diffFilter?: string,
  exclude?: string[]
}): Promise<string> => {
  const git = getGitInstance(repoPath);

  if(staged && (from !== undefined || to !== undefined)){
    throw new Error("'staged' cannot be combined with 'from' or 'to'");
  }

  if(from === undefined && to !== undefined){
    throw new Error("'from' param is required when 'to' is present");
  }

  const args: string[] = [];

  if (staged) args.push("--cached");
  if(from !== undefined) args.push(from);
  if(to !== undefined) args.push(to);

  args.push(format);

  if(detectRenames === true) args.push("-M");
  if(detectRenames === false) args.push("--no-renames");
  if(reverse) args.push("-R");

  if (files?.length) {
    args.push("--", ...files);
  } else if (exclude?.length) {
    args.push("--", ".");
  }

  if(exclude.length > 0) {
    exclude.forEach((e) => {
      args.push(`:(exclude)${e}`)
    })
  }

  const response = await git.diff(args);
  return "response";
}

// export const read_file = ({
//   repoPath
// }: {

// }): string => {
//   const git = getGitInstance(repoPath);
//   return "something"
// }

git_log({
  format: CommitFormat.email,
});

git_diff({
  from: "4915b743424b7ef444f07b66e06d4f5e177c0502",
  to: "add00cd8e3e3650f1f4114a4d6042dfca037e7c2",
  exclude: ["package-lock.json"],
});