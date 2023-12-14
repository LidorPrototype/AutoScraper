export class ScrapeRequest {
    PartitionKey!: number;
    RowKey!: number;
    DAG_Name!: string;
    DestinationID!: number;
    cron!: string;
    description!: string;
    end_date!: string;
    output_name!: string;
    serviceID!: number;
    start_date!: string;
    status!: string;
    user!: string;
    changed!: boolean;
    originalStatus!: string;
}

export class UsersScreen {
    PartitionKey!: number;
    RowKey!: number;
    DAG_Name!: string;
    DestinationID!: number;
    cron!: string;
    description!: string;
    end_date!: string;
    output_name!: string;
    serviceID!: number;
    start_date!: string;
    status!: string;
    user!: string;
    actions!: string;
}

export class LogsRequest {
    PartitionKey!: number;
    RowKey!: number;
    DAG_Name!: string;
    DestinationID!: number;
    cron!: string;
    description!: string;
    user!: string;
    Date!: string;
}