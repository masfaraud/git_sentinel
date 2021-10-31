export interface Repository {
  id: number;
  name: string;
  active: boolean;
}


export interface Issue {
  id: number;
  title: string;
  type: string;
  priority: string;
  repository: Repository;
}
