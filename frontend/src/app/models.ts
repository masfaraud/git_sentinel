export interface EmailAddress {
  id: number;
  address: string;
}

export interface DeveloperAccount {
  id: number;
  full_name: string;
  login: string;
  email_addresses: EmailAddress;
}

export interface Developer {
  id: number;
  full_name: string;
  accounts: DeveloperAccount[];
  assignee_repositories: Repository[];
  assignee_issues: Issue[];
  number_issues_solved: number;
  number_open_issues_assigned: number;
}

export interface Repository {
  id: number;
  name: string;
  active: boolean;
  assignees: Developer[];
  issues: Issue[];
}


export interface Issue {
  id: number;
  title: string;
  type: string;
  body: string;
  priority: string;
  repository: Repository;
}

export interface PullRequest {
  id: number;
  title: string;
  body: string;
  repository: Repository;
  base_branch: string;
  head_branch: string;
}
