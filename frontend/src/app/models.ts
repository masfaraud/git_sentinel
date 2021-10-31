export interface EmailAddress {
  id: number;
  address: string;
}

export interface Developer {
  id: number;
  first_name: string;
  last_name: string;
  email_addresses: EmailAddress[];
}


export interface Repository {
  id: number;
  name: string;
  active: boolean;
  assignees: Developer[];
}


export interface Issue {
  id: number;
  title: string;
  type: string;
  priority: string;
  repository: Repository;
}
