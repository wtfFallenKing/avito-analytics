import { useMemo } from 'react';
import { useQuery } from 'react-query';
import type { Node } from '~/entities';

export function useNodeChoices(resource: string, queryFn: () => Promise<any>) {
  const { data, isLoading, error } = useQuery([resource, 'getMany'], queryFn);

  const choices = useMemo(
    () =>
      data
        ? (data as Node[]).map((node) => ({
            id: node.id,
            name: node.name,
          }))
        : [],
    [data],
  );

  return {
    choices,
    isLoading,
    error,
  };
}
