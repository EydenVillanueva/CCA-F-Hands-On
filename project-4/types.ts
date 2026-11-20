export enum CommitFormat {
  oneline= "oneline",
  short = "short",
  medium = "medium",
  full = "full", 
  fuller = "fuller",
  email = "email",
  raw = "raw"
}

export enum DiffFormat {
  patch = "--patch",
  stat = "--stat",
  numstat = "--numstat",
  nameOnly = "--name-only",
  nameStatus = "--name-status",
  summary = "--summary",
}