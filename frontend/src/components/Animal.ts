
//for the animal list
export interface AnimalSummary {
    id: number;
    name: string;
    type: string;
    breed?: string;
    status: string;
    reward?: number;
    photo: string;
  }
  
  //for the animal card
  export interface AnimalDetails extends AnimalSummary {
    location: string;
    owner: string;
    postLink: string;
    description: string;
  }
